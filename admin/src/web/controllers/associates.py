import math
from datetime import datetime, date
import base64
import qrcode
from pathlib import Path
import os
import bcrypt
import pdfkit

import pandas as pd
from flask import Blueprint
from flask import flash
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import make_response
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import EmailField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.validators import Length, NumberRange

from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.core import associates
from src.core import payments
from src.core import adminConfig
from src.core import disciplines


associates_blueprint = Blueprint(
    'associates', __name__, url_prefix='/associates')


class associateEditForm(FlaskForm):
    """Formulario del update de los asociados"""

    name = TextAreaField('Nombre:', validators=[DataRequired(), Length(
        4, 30)], render_kw={"rows": 1})
    surname = TextAreaField('Apellido:', validators=[
                            DataRequired(), Length(4, 30)], render_kw={"rows": 1, "cols": 1})
    document_type = SelectField('Tipo de documento', validators=[DataRequired()],
                                choices=[('dni', 'Documento Nacional de Identidad'), ('lc', 'Libreta Cívica'),
                                         ('le', 'Libreta de Enrolamiento'), ('ci', 'Cédula de identidad')])
    document_number = TextAreaField('Numero de Documento', validators=[
        DataRequired(), Length(4, 8)], render_kw={"rows": 1})
    gender = SelectField('Genero', validators=[DataRequired()],
                         choices=[('f', 'Femenino'), ('m', 'Masculino'), ('otro', 'Otro')])
    address = TextAreaField('Direccion', validators=[DataRequired(),
                                                     Length(1, 30)])
    phone_number = TextAreaField('Numero de telefono', validators=[Length(0, 20)]
                                 )
    email = EmailField('Correo electronico', validators=[Length(0, 50)]
                       )


class associateNewForm(FlaskForm):
    """Formulario para la creación de asociados"""

    name = TextAreaField('Nombre:', validators=[DataRequired(), Length(
        4, 30)], render_kw={"rows": 1})
    surname = TextAreaField('Apellido:', validators=[
                            DataRequired(), Length(4, 30)], render_kw={"rows": 1, "cols": 1})
    document_type = SelectField('Tipo de documento', validators=[DataRequired()],
                                choices=[('dni', 'Documento Nacional de Identidad'), ('lc', 'Libreta Cívica'),
                                         ('le', 'Libreta de Enrolamiento'), ('ci', 'Cédula de identidad')])
    document_number = IntegerField(
        'Numero de documento', validators=[DataRequired(), NumberRange(1000, 99999999)])
    gender = SelectField('Genero', validators=[DataRequired()],
                         choices=[('f', 'Femenino'), ('m', 'Masculino'), ('otro', 'Otro')])
    address = TextAreaField('Direccion', validators=[DataRequired(),
                                                     Length(1, 30)])
    phone_number = IntegerField(
        'Numero de telefono:', validators=[DataRequired(), NumberRange(0, 2147483647)])
    email = EmailField('Correo electronico', validators=[Length(0, 50)]
                       )
    date_of_birth = DateField(
        'Fecha de nacimiento:', validators=[DataRequired()])


@associates_blueprint.get('/<int:page>')
@login_required
@permission_required
def associates_index(page):
    """Esta funcion nos lleva a la lista de los asociados del sistema
    haciendo su respectiva paginación."""

    form_inscripcion = inscriptions_form()
    amount, associ = associates.list_associates(page)

    config = adminConfig.list_config()
    nums = math.ceil(amount/config.cant_elementos)
    if (page < 1 and nums > 0):
        flash("La página solicitada no existe", "danger")
        return render_template('associates/associate_list.html',  form_inscripcion=form_inscripcion, associates=associ, nums=nums, page=int(page))

    if (page > nums):
        flash("La página solicitada no existe", "danger")
    elif (len(associ) < 1):
        flash("Parece que aún no hay asociados creados 😅", "warning")

    return render_template('associates/associate_list.html', associates=associ, form_inscripcion=form_inscripcion, nums=nums, page=int(page), filter=False)


@associates_blueprint.get('/filter')
@login_required
def associates_filtered_index():
    """Esta funcion nos lleva a una version del index filtrada por
    parametros que le llegan mediando el metodo GET"""

    params = request.args
    page = int(params['page'])
    surname = params['surname']
    state = params['state']

    if surname == '' and state == '':
        return redirect(url_for("associates.associates_index", page=1))

    if surname == '':
        amount, associ = associates.list_associates_filter_by_status(
            page, state)
    elif state == '':
        amount, associ = associates.list_associates_filter_by_surname(
            page, surname)
    else:
        amount, associ = associates.list_associates_filter_by_surname_and_status(
            page, surname, state)

    config = adminConfig.list_config()
    nums = math.ceil(amount/config.cant_elementos)
    form_inscripcion = inscriptions_form()
    if (len(associ) < 1):
        flash("No se han encontrado asociados con los atributos especificados", 'warning')

    return render_template('associates/associate_list.html', form_inscripcion=form_inscripcion, associates=associ, nums=nums, page=int(page), surname=surname, state=state, filter=True)


@associates_blueprint.get('/new')
@login_required
@permission_required
def associates_new():
    """Esta funcion renderiza el formulario para poder crear un nuevo asociado"""

    form = associateNewForm()

    return render_template('associates/create_associate.html', form=form)


@associates_blueprint.post('/new')
@login_required
def create_new_associate():
    """Función de creación de un nuevo asociado"""

    form = associateNewForm(request.form)
    if (form.validate()):
        # Tomo los valores del formulario
        name = request.form.get('name').strip()
        surname = request.form.get('surname').strip()
        document_type = request.form.get('document_type')
        document_number = request.form.get('document_number').strip()
        gender = request.form.get('gender')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address').strip()
        phone_number = request.form.get('phone_number').strip()
        email = request.form.get('email').strip().lower()
        # Creo el usuario
        if associates.find_associate_by_dni(document_number):
            flash(
                "Ya existe un asociado con el mismo número de documento, ingrese otro", "danger")
        else:
            assoc = associates.create_associate(
                name=name,
                surname=surname,
                document_type=document_type,
                document_number=document_number,
                gender=gender,
                address=address,
                phone_number=phone_number,
                email=email,
                date_of_birth=date_of_birth,
                password=(bcrypt.hashpw(str.encode(document_number),
                                        bcrypt.gensalt(12))).decode('utf-8')
            )

            today = date.today()
            months_year = [(f.month, f.year)for f in assoc.fees]
            # Traigo de la config el costo base
            config = adminConfig.list_config()
            base_cost = config.valor_cuota_base
            for m in range(today.month, 12):
                if (m+1, today.year) not in months_year:  # Si la cuota no fue creada, la creo
                    payments.create_fee(
                        year=today.year,
                        month=m + 1,
                        amount_to_pay=base_cost,
                        paid=False,
                        expiration_date=date(today.year, m + 1, 10),
                        associate_id=assoc.id
                    )
            flash("Usuario creado con éxito", "success")
    else:
        flash("Ocurrió un error al validar los campos, inténtelo nuevamente", "danger")
    return redirect(url_for("associates.associates_index", page=1))


@associates_blueprint.get('/<int:id>/edit')
@login_required
@permission_required
def associates_update(id):
    """Esta funcion se utiliza para actualizar los atributos del asociado"""

    associ = associates.get_associate_by_id(id)
    form = associateEditForm(
        email=associ.email,
        name=associ.name,
        surname=associ.surname,
        gender=associ.gender,
        address=associ.address,
        phone_number=associ.phone_number,
        document_type=associ.document_type,
        document_number=associ.document_number
    )
    return render_template('associates/associate_update.html', associ=associ, form=form)


@associates_blueprint.post('/<int:id>/edit')
@login_required
def edit_associate(id):
    """Este metodo captura los campos del formulario, los valida
    y si son correctos actualiza los campos del asociado.       """

    form = associateEditForm(request.form)
    if (form.validate()):
        name = request.form.get('name').strip()
        surname = request.form.get('surname').strip()
        document_type = request.form.get('document_type')
        document_number = request.form.get('document_number').strip()
        gender = request.form.get('gender')
        address = request.form.get('address').strip()
        phone_number = request.form.get('phone_number').strip()
        email = request.form.get('email').strip().lower()

        assoc_aux = associates.find_associate_by_dni(document_number)
        if assoc_aux != None and assoc_aux.id != id:
            flash(
                "Ya existe un usuario con el mismo DNI, ingrese otro", "danger")
        else:
            associates.update_associate(
                id, surname, email, name, phone_number, address, gender, document_number, document_type)
            flash("Usuario actualizado con éxito", "success")
    else:
        flash("Ocurrió un error al validar los campos, inténtelo nuevamente", "danger")
    return redirect(url_for("associates.associates_index", page=1))


@associates_blueprint.post('/<int:id>/delete')
@login_required
@permission_required
def associates_destroy(id):
    """Esta funcion elimina un asociado del sistema"""

    associates.delete_associate_by_id(id)
    flash("Usuario eliminado con éxito", "success")
    return redirect(url_for("associates.associates_index", page=1))


@associates_blueprint.get('/<int:id>/show')
@login_required
@permission_required
def associates_show(id):
    """Esta funcion muestra mas informacion sobre el asociado que se le indique"""

    associ = associates.get_associate_by_id(id)
    return render_template("associates/associate_show.html",  associate=associ)


@associates_blueprint.post('/export')
@login_required
def associates_export():
    """Funcion que exporta la lista de asociados, ya sea completa o por algun filtro en particular"""

    params = request.form

    surname = params['surname']
    state = params['state']
    if state != '' or surname != '':
        if surname == '':
            associ = associates.list_all_associates_filter_by_status(state)
        elif state == '':
            associ = associates.list_all_associates_filter_by_surname(surname)
        else:
            associ = associates.list_all_associates_filter_by_surname_and_status(
                surname, state)
    else:
        associ = associates.list_all_associates()

    if associ == []:
        flash("No puede exportar una documento vacío", 'warning')
        return redirect(url_for('associates.associates_index', page=1))
    else:
        if (params['export'] == "csv"):
            df = pd.DataFrame.from_records([a.to_dict() for a in associ])

            response = make_response(df.to_csv())
            response.headers["Content-Disposition"] = "attachment; filename=asociados.csv"
            response.headers["Content-Type"] = "text/csv"
        elif (params['export'] == 'pdf'):
            html = render_template(
                "associates/export_associates.html", associates=associ)
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
            response.headers['Content-Disposition'] = 'inline; filename=asociados.pdf'
        flash("Asociados exportados exitosamente", "success")
        return response


@associates_blueprint.post('/edit_status/<int:id>')
@login_required
def toggle_status_associate(id):
    """Esta funcion cambia el estado del asociado por el contrario que tenga
    al momento de llamar la funcion"""

    asso = associates.get_associate_by_id(id)

    if (asso.status == True):
        status = False
        associates.update_status(status, id)
    else:
        status = True
        associates.update_status(status, id)

    flash("Se ha actualizado el estado del asociado", "success")
    return redirect(url_for("associates.associates_index", page=1))


@associates_blueprint.post('<int:id>/card/')
@login_required
def card_new(id):
    """Esta funcion carga el formulario para la creacion de un carnet"""
    img = request.files.get('image')
    if img:
        path_img = os.path.abspath(os.path.join(
            Path(__file__), '..', '..', '..', '..',   "private", "photos"))
        img.save(f'{path_img}/{id}.jpeg')
        data = 'https://admin-grupo16.proyecto2022.linti.unlp.edu.ar' + \
            url_for("associates.associates_show", id=id)
        qr = qrcode.make(data)
        path_qr = os.path.abspath(os.path.join(
            Path(__file__), '..', '..', '..', '..', "private", "qrs"))
        qr.save(f'{path_qr}/{id}.png')
        associates.update_card_date(id, datetime.now())
    else:
        flash("No ha adjuntado una foto", "warning")

    return redirect(url_for("associates.associates_show", id=id))


@associates_blueprint.get('/card/<int:id>')
@login_required
def export_card(id):

    moroso = False
    associate = associates.get_associate_by_id(id)
    fees = associate.fees
    for f in fees:
        if (not f.paid) and (date.fromisoformat(str(f.expiration_date)) < date.today()):
            moroso = True
            break

    QR = os.path.abspath(os.path.join(Path(__file__), '..',
                         '..', '..', '..', "private", "qrs", f"{id}.png"))

    logo = os.path.abspath(os.path.join(
        Path(__file__), '..', '..', '..', '..', "public", "img", "logo_carnet.png"))

    img = os.path.abspath(os.path.join(
        Path(__file__), '..', '..', '..', '..',   "private", "photos", f"{id}.jpeg"))

    html = render_template("associates/associate_carnet.html",
                           associate=associate, moroso=moroso, qr=QR, image=img, logo=logo)

    options = {
        "orientation": "portrait",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
        "--enable-local-file-access": None,

    }
    binary_pdf = pdfkit.from_string(html, options=options)
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


class CreateForm(FlaskForm):
    """Formulario de creacion de inscripción a disciplinas"""

    Asociado = SelectField(
        'Elegí un asociado:', validators=[DataRequired()])
    Disciplina = SelectField(
        'Elegí una disciplina:', validators=[DataRequired()])


def inscriptions_form():
    """Crea el formulario de inscripción"""

    avaliable_disciplines = disciplines.list_all_enabled_disciplines()
    available_associates = associates.list_active_associates()
    group_disciplines = [(i.id, i.name + " - " + str(i.monthly_price))
                         for i in avaliable_disciplines]
    group_associates = [(i.id, i.name + " - " + i.surname+" - "
                         + i.address) for i in available_associates]
    form_create = CreateForm()
    form_create.Asociado.choices = group_associates
    form_create.Disciplina.choices = group_disciplines
    return form_create
