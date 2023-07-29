import math
from datetime import date

from flask import Blueprint
from flask import render_template
from flask import flash
from flask import request
from flask import make_response
from flask import url_for
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
import pdfkit

from src.core import adminConfig
from src.core import associates
from src.core import payments
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required


payments_blueprint = Blueprint('payment', __name__, url_prefix='/payments')


class SearchForm(FlaskForm):
    text_for_search = TextAreaField('Nro. Asociado/Apellido', validators=[DataRequired(), Length(1, 40)], render_kw={"rows": 1, "cols": 2})
    search_by_id = SelectField('Buscar por:', choices=[("True", "Nro. asociado"), ("", "Apellido")])


class ReceiptNewForm(FlaskForm):
    paid_by = TextAreaField('¿Quién pagó esta cuota?: ', validators=[DataRequired(), Length(4, 32)], render_kw={"rows": 1, "cols": 1})


@payments_blueprint.get("/")
@login_required
@permission_required
def payments_index():
    form = SearchForm(text_for_search="")
    return render_template("payments/payments_manage.html", form=form)


@payments_blueprint.get("/generate_installments")
@login_required
@permission_required
def payments_create_fee():
    """Genera las cuotas del año actual  para
    cada asociado. Las cuotas se registran como impagas
    en un principio, cuando se registren los pagos cam-
    biaran de estado. Las cuotas vencen el  dia  10  de
    cada mes."""

    form = SearchForm(text_for_search="")
    #Tengo que generar las cuotas para todo el año para cada asociado.
    associates_list = associates.list_all_associates()
    today = date.today()
    for a in associates_list:
        months_year = [(f.month, f.year)for f in a.fees]
        #Calculo el costo de las disciplinas que practica el asociado
        cost_of_disciplines = 0
        for d in a.disciplines_practiced:
            cost_of_disciplines = cost_of_disciplines + d.monthly_price
        #Traigo de la config el costo base
        config = adminConfig.list_config()
        base_cost = config.valor_cuota_base
        #Calculo el monto de la cuota
        total_amount = float(base_cost) + cost_of_disciplines
        for m in range(today.month, 12):
            if (m+1,today.year) not in months_year: # Si la cuota no fue creada, la creo
                payments.create_fee(
                    year = today.year,
                    month = m + 1,
                    amount_to_pay = total_amount,
                    paid = False,
                    expiration_date = date(today.year, m + 1, 10),
                    associate_id = a.id
                )
    flash("Se han creado las cuotas para este año correctamente", "success")
    return render_template("payments/payments_manage.html", form=form)


@payments_blueprint.get("/get_slow_payer")
@login_required
@permission_required
def associates_show():
    """Muestro por pantalla la lista de asociados morosos, o
    sea que no estan al dia con las cuotas del club."""

    form = SearchForm(text_for_search=request.form.get('text_for_search'))

    #Me traigo los asociados y sus cuotas
    associates_list = associates.list_all_associates()
    slow_payers_list = []
    for a in associates_list:

        fees = a.fees

        #Me fijo si el asociado es un moroso, si lo es lo agrego a una lista
        for f in fees:
            if (not f.paid) and (date.fromisoformat(str(f.expiration_date)) < date.today()):
                slow_payers_list.append(a)
    if len(slow_payers_list) == 0:
        flash("No hay asociados morosos en el sistema!", "success")
        return render_template("payments/payments_manage.html", form=form, associates=slow_payers_list, show_modal=False)
    
    return render_template("payments/payments_manage.html", form=form, associates=slow_payers_list, show_modal=True)


@payments_blueprint.get("/get_asociate_fees/<int:id>/<int:page>")
@login_required
@permission_required
def payments_show_fees(id, page):
    """El objetivo es mostrar las cuotas del asociado."""

    #Me traigo al asociado y sus cuotas
    associate = associates.get_associate_by_id(id)
    fees = associate.fees

    form = ReceiptNewForm(paid_by=associate.name + ' ' + associate.surname)

    #Me fijo si el asociado es un moroso
    moroso = False
    for f in fees:
        if (not f.paid) and (date.fromisoformat(str(f.expiration_date)) < date.today()):
            moroso = True
            break


    config = adminConfig.list_config()
    surcharge = (config.porcentaje_recargo) * 0.01

    # (porcentaje_recargo * 0.01 * total_amount -> surcharge)

    #Calculo el nro. de paginas
    nums = math.ceil(len(fees) / config.cant_elementos)

    #Me traigo la lista de cuotas paginada
    fees = payments.get_fees_by_associate_id_paged(id, page)

    return render_template("payments/payments_list.html", form=form, today=date.today(), nums=nums, page=page, surcharge=surcharge, associate=associate, fees=fees, slow_payer=moroso, months=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])


@payments_blueprint.post("/get_asociate_payments")
@login_required
@permission_required
def payments_search_associate_fees():
    """El objetivo es mostrar las cuotas del asociado. La
    busqueda puede ser por id (unico asociado)  o por ape-
    llido (puede haber mas).  En el caso de que de la bus-
    queda  resulten  varios  asociados se imprime un modal
    que los lista para elegir cual asociado deseamos ver.
    """

    form = SearchForm(request.form)
    if (form.validate()):
        search_by_id = bool(request.form.get('search_by_id'))
        associates_list = []
        if search_by_id:
            """En este caso busco un asociado particular, por
            lo que me dirijo a una nueva pantalla donde se
            listan sus cuotas."""
            
            try:
                associate_id = int(request.form.get('text_for_search'))
            except ValueError:
                flash("El nro. de asociado debe ser un número!!!", "danger")
                associate_id = None
            if associate_id != None:
                
                #Busco al asociado por su id
                associate = associates.get_associate_by_id(associate_id)

                if associate != None:
                    return redirect(url_for('payment.payments_show_fees', id=associate_id, page=1))
                else:
                    flash("No existe ningún asociado con el id indicado", "danger")
                    return render_template("payments/payments_manage.html", form=form, associates=[], show_modal=False)
        else:
            """En el caso de que la búsqueda sea por apellido,
            imprimo una ventana modal en donde listo a todos
            los asociados que tienen ese apellido."""
            
            associate_surname = str(request.form.get('text_for_search'))
            
            """Primero me traigo la lista de  asociados,  filtro  por  apellido,
            si existe un solo asociado me voy directo a la vista  de  pagos,  si
            no hay asociados con ese apellido imprimo un  flash  y  si  hay  mas
            de un asociado con  ese  apellido  muestro  un  modal  para  que  el
            usuario elija el asociado correcto del cual quiere ver sus pagos."""

            filtered_list = associates.list_all_associates_filter_by_surname(associate_surname) # %LIKE
            result_count = len(filtered_list)

            if (result_count == 1):
                associate = list(filtered_list)[0]
                return redirect(url_for('payment.payments_show_fees', id=associate.id, page=1))
            elif (result_count == 0):
                flash("No se encontraron asociados con ese apellidos", "danger")
            else:
                return render_template("payments/payments_manage.html", form=form, associates=filtered_list, show_modal=True)

    else:
        flash("Hubo un problema con los datos ingresados, intente más tarde.", "danger")

    return render_template("payments/payments_manage.html", form=form, show_modal=False)


@payments_blueprint.post("/create_fee_receipt/<int:id_fee>/<int:id_associate>/<float:total_amount>")
@login_required
@permission_required
def payments_create_fee_receipt(id_fee, id_associate, total_amount):
    """Creo un recibo de pago para la cuota
    recibida."""
    
    #Me traigo al asociado
    associate = associates.get_associate_by_id(id_associate)

    if associate:
        
        first_fee = sorted(filter(lambda f: f.paid == False, associate.fees), key=lambda f : (f.year, f.month))[0]

        if first_fee.id == id_fee:

            #Capturo el nombre de quien paga
            paid_by = request.form.get('paid_by')

            #Creo un recibo para el pago efectuado
            receipt = payments.create_receipt(
                payment_date=date.today(),
                amount_paid=total_amount,
                paid_by=paid_by,
                fee=first_fee
            ) 

            #Registro como paga la cuota
            payments.pay_fee_and_assign_receipt(first_fee, receipt)


            flash("La cuota se pagó exitosamente", "success")
        else:
            flash("No puede pagar esta cuota sin pagar las anteriores", "warning")

    return redirect(url_for('payment.payments_show_fees', id=id_associate, page=1))


@payments_blueprint.get("/create_pdf_receipt/<int:id_fee>/<int:id_associate>")
@login_required
@permission_required
def payments_export_fee_receipt(id_fee, id_associate):
    """Creo un recibo de pago para la cuota
    recibida."""

    #Me traigo la cuota
    fee = payments.get_fee_by_id(id_fee)

    #Me traigo al asociado
    associate = associates.get_associate_by_id(id_associate)

    config = adminConfig.list_config()
    #Chequeo si la cuota vencio al momento del pago
    moroso = False
    fee_receipt = fee.receipt

    if date.fromisoformat(str(fee.expiration_date)) < date.fromisoformat(str(fee_receipt.payment_date).split(' ')[0]):
        moroso = True

    html = render_template("payments/payments_pdf_receipt.html", fee=fee, associate=associate, total_amount=fee_receipt.amount_paid, slow_payer=moroso, months=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], frase=config.texto_recibo)

    #A partir del html renderizado hago un pdf renderizado y lo envio como response
    options = {
        "orientation": "portrait",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }
    binary_pdf = pdfkit.from_string(html, options=options)
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response