from datetime import date

from flask import Blueprint
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length

from src.web.helpers.auth import login_required
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.core import adminConfig
from src.core import associates
from src.core import payments


config_blueprint = Blueprint('config', __name__, url_prefix='/config')


@config_blueprint.get('/')
@login_required
@permission_required
def config_index():
    """Muestra la configuración en /config"""

    configuracion = adminConfig.list_config()
    form = ConfigForm(
        cant_elementos=configuracion.cant_elementos, informacion_contacto=configuracion.info_contacto,
        texto_recibo=configuracion.texto_recibo, valor_cuota=configuracion.valor_cuota_base,
        recargo=configuracion.porcentaje_recargo)
    return render_template('config.html', config=configuracion, form=form)


class ConfigForm(FlaskForm):
    """Formulario de modificación de la configuración"""

    cant_elementos = IntegerField(
        'Cantidad de elementos por página', validators=[DataRequired(), NumberRange(1, 1000)])
    habilitar_pagos = SelectField(
        '¿Habilitar pagos?', choices=[("True", "Si"), ("", "No")])
    informacion_contacto = TextAreaField(
        'Información de contacto:', validators=[DataRequired(), Length(5, 255)], render_kw={"rows": 2, "cols": 2})
    texto_recibo = TextAreaField(
        'Texto para el recibo:', validators=[DataRequired(), Length(5, 255)], render_kw={"rows": 2, "cols": 2})
    valor_cuota = DecimalField(
        'Valor cuota base:', validators=[DataRequired(), NumberRange(1, 2147483647)])
    recargo = IntegerField(
        'Porcentaje de recargo para morosos:', validators=[DataRequired(), NumberRange(0, 2147483647)])


@ config_blueprint.post('/')
@login_required
@permission_required
def config_update():
    """Captura los valores del form y los usa para modificar la configuración"""

    form = ConfigForm(request.form)
    if (form.validate()):
        cant_elementos = request.form.get('cant_elementos')
        pago_habilitado = bool(request.form.get('habilitar_pagos'))
        info_contacto = request.form.get('informacion_contacto')
        texto_recibo = request.form.get('texto_recibo')
        valor_cuota_base = request.form.get('valor_cuota')

        config_actual = adminConfig.list_config()
        if (config_actual.valor_cuota_base != float(valor_cuota_base)):
            assocs = associates.list_all_associates()
            for a in assocs:
                cost_of_disciplines = 0
                for d in a.disciplines_practiced:
                    cost_of_disciplines = cost_of_disciplines + d.monthly_price
                # Calculo el monto de la cuota
                actual_amount = float(valor_cuota_base) + cost_of_disciplines
                # Actualizo la cantidad en las cuotas del asociado a partir del mes que viene
                fees = a.fees
                today = date.today()
                for f in fees:
                    if ((not f.paid) and f.month > today.month and f.year == today.year):
                        payments.update_fee_amount(f, actual_amount)

        porcentaje_recargo = request.form.get('recargo')
        flash("Se guardó el contenido con éxito", "success")
        adminConfig.update_config(
            cant_elementos,
            pago_habilitado,
            info_contacto,
            texto_recibo,
            valor_cuota_base,
            porcentaje_recargo)
    else:
        flash("No se pudo guardar el contenido, ocurrió un error al validar los campos", "danger")
    return redirect(url_for("config.config_index"))
