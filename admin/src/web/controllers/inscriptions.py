from datetime import date
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import url_for
from flask import request

from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.core import associates
from src.core import payments
from src.core import adminConfig


inscriptions_blueprint = Blueprint(
    'inscriptions', __name__, url_prefix='/inscriptions')


@inscriptions_blueprint.post('/<int:page>')
@login_required
@permission_required
def inscriptions_make(page):
    """Inscribe a un asociado en la disciplina correspondiente"""

    if (request.form.get('Asociado') and request.form.get('Disciplina')):
        assoc = associates.get_associate_by_id(request.form.get('Asociado'))
        # Me fijo si el asociado es un moroso
        moroso = False
        for f in assoc.fees:
            if (not f.paid) and (date.fromisoformat(str(f.expiration_date)) < date.today()):
                moroso = True
                break

        if (not moroso):
            res = associates.create_inscription(int(request.form.get(
                'Asociado')), request.form.get(
                'Disciplina'))
            if (res):
                cost_of_disciplines = 0
                for d in assoc.disciplines_practiced:
                    cost_of_disciplines = cost_of_disciplines + d.monthly_price
                # Calculo el monto de la cuota
                valor_cuota_base = adminConfig.list_config().valor_cuota_base
                actual_amount = float(valor_cuota_base) + cost_of_disciplines
                # Actualizo la cantidad en las cuotas del asociado a partir del mes que viene
                fees = assoc.fees
                today = date.today()
                for f in fees:
                    if ((not f.paid) and f.month > today.month and f.year == today.year):
                        payments.update_fee_amount(f, actual_amount)
                flash("Se inscribió al asociado con éxito", "success")
            else:
                flash(
                    "El asociado ya se encuentra inscripto en esa disciplina", "danger")
        else:
            flash(
                "El asociado es moroso, no puede ser inscripto a disciplinas hasta que deje de serlo", "danger")
    else:
        flash("Completa los campos", "danger")

    return redirect(url_for("associates.associates_index", page=page))
