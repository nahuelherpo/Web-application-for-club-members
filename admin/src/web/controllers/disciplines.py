from datetime import date

from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import flash
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange, Length

from src.core import adminConfig
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.core import disciplines
from src.core import payments

disciplines_blueprint = Blueprint(
    'disciplines', __name__, url_prefix='/disciplines')


class CreateForm(FlaskForm):
    """Formulario para la creación de una disciplina"""

    name = StringField(
        'Nombre:', validators=[DataRequired(), Length(min=1, max=1000)])
    monthly_price = DecimalField(
        'Precio mensual:', validators=[DataRequired(), NumberRange(1, 2147483647)])


class CreateEditForm(FlaskForm):
    """Formulario para la edición de una disciplina"""

    new_name = StringField(
        'Nuevo nombre:', validators=[DataRequired(), Length(min=1, max=1000)])
    new_monthly_price = DecimalField(
        'Nuevo precio mensual:', validators=[DataRequired(), NumberRange(1, 2147483647)])
    id_anterior = IntegerField('id_anterior', validators=[DataRequired()])


@disciplines_blueprint.get('/<int:page>')
@login_required
@permission_required
def disciplines_show(page):
    """Muestra las disciplinas usando la paginación en /disciplinas/pagina"""

    nums = disciplines.paginated_quantity_discipline()
    if (page < 1):
        flash("La página solicitada no existe", "danger")
        return redirect(url_for("disciplines.disciplines_show", page=1))
    if (page > nums and nums > 0):
        flash("La página solicitada no existe", "danger")
        return redirect(url_for("disciplines.disciplines_show", page=1))
    form = CreateForm()
    form_edit = CreateEditForm()
    dis = disciplines.list_disciplines(page)
    return render_template('disciplines/disciplines.html', disciplines=dis, nums=nums, page=int(page), form=form, form_edit=form_edit)


@disciplines_blueprint.post('/<int:page>')
@login_required
@permission_required
def disciplines_new(page):
    """Valida que el formulario para crear una disciplina sea correcto y la crea"""

    form = CreateForm(request.form)
    if (form.validate()):
        new_dis = disciplines.create_discipline(name=request.form.get(
            'name'), monthly_price=request.form.get('monthly_price'), enabled=True)
        flash("Se creó la disciplina con éxito", "success")
        return disciplines_index(new_dis.id)
    flash("Ocurrió un error al validar los campos", "danger")
    return disciplines_show(page)


class CreateCategoryForm(FlaskForm):
    """Formulario para la creación de una categoría"""

    name_category = StringField(
        'Nombre de la categoría:', validators=[DataRequired(), Length(min=1, max=1000)])
    instructor_category = StringField(
        'Nombre del instructor:', validators=[DataRequired(), Length(min=1, max=1000)])
    days_category = StringField(
        'Día de categoría:', validators=[DataRequired(), Length(min=1, max=1000)])
    hour_fence_category = StringField(
        'Horario:', validators=[DataRequired(), Length(min=1, max=1000)])


class CreateAddCategoryForm(FlaskForm):
    """Formulario para agregar una categoría a una disciplina"""

    selected_category = SelectField(
        'Elegí una categoría:', validators=[DataRequired()])


@disciplines_blueprint.get('/id/<int:id>')
@login_required
@permission_required
def disciplines_index(id):
    """Pagina detalle de una disciplina en /discipline/id"""

    res = disciplines.detail_discipline(id)
    available_categories = disciplines.list_categories()
    form = CreateCategoryForm()
    form2 = CreateAddCategoryForm()
    groups_list = [(i.id, i.name + " - " + i.instructors+" - "+i.days +
                   " - " + i.hour_fence) for i in available_categories]
    form2.selected_category.choices = groups_list
    if (res[0] is None):
        flash("No existe la disciplina solicitada", "danger")
        return redirect(url_for("disciplines.disciplines_show", page=1))
    else:
        return render_template('disciplines/discipline_detail.html', discipline=res[0], categories=res[1], form=form, form2=form2, available_categories=available_categories)


@disciplines_blueprint.post('/id/<int:id>')
@login_required
@permission_required
def discipline_create_categorie(id):
    """Controlador para crear una categoría y añadirla a una disciplina"""

    form = CreateCategoryForm(request.form)
    if (form.validate()):
        disciplines.create_and_add_category(name=request.form.get(
            'name_category'), instructors=request.form.get(
            'instructor_category'), days=request.form.get(
            'days_category'), hour_fence=request.form.get(
            'hour_fence_category'), id=id)
        flash("Se creó y se agregó la categoría con éxito", "success")
    else:
        flash("Ocurrió un error de validación", "danger")
    return redirect(url_for("disciplines.disciplines_index", id=id))


@disciplines_blueprint.post('/add/<int:id>')
@login_required
@permission_required
def discipline_add_categorie(id):
    """Controlador para añadir una categoría ya existente a una disciplina"""

    if (not (request.form.get(
            'selected_category') is None)):
        res = disciplines.add_category(id, int(request.form.get(
            'selected_category')))
        if (res):
            flash("Esta categoría ya existe en esta disciplina", "warning")
        else:
            flash("Se agregó correctamente", "success")
    else:
        flash("Ocurrió un error en la validación", "danger")
    return redirect(url_for("disciplines.disciplines_index", id=id))


@disciplines_blueprint.post('/edit/<int:page>')
@login_required
@permission_required
def disciplines_update(page):
    """Controlador para editar una disciplina"""

    form = CreateEditForm(request.form)
    if (form.validate()):
        id_dis = int(request.form.get('id_anterior'))
        dis = disciplines.get_discipline_by_id(id_dis)
        new_monthly_price = float(request.form.get('new_monthly_price'))
        if (dis.monthly_price != new_monthly_price):
            assocs = dis.associates_enrolled
            for a in assocs:
                cost_of_disciplines = 0
                for d in a.disciplines_practiced:
                    if (d.id == id_dis):
                        cost_of_disciplines = cost_of_disciplines + new_monthly_price
                    else:
                        cost_of_disciplines = cost_of_disciplines + d.monthly_price
                # Calculo el monto de la cuota
                valor_cuota_base = adminConfig.list_config().valor_cuota_base
                actual_amount = float(valor_cuota_base) + cost_of_disciplines
                # Actualizo la cantidad en las cuotas del asociado a partir del mes que viene
                fees = a.fees
                today = date.today()
                for f in fees:
                    if ((not f.paid) and f.month > today.month and f.year == today.year):
                        payments.update_fee_amount(f, actual_amount)
        disciplines.edit_discipline(int(request.form.get(
            'id_anterior')), request.form.get(
                'new_name'), request.form.get(
                    'new_monthly_price'))
        flash("Se editó la disciplina", "success")
    else:
        flash("Ocurrió un error", "danger")

    return redirect(url_for("disciplines.disciplines_show", page=page))


@disciplines_blueprint.post('/disable/<int:id>/<int:page>')
@login_required
@permission_required
def disciplines_update_enabled(id, page):
    """Controlador para habilitar/deshabilitar una disciplina"""

    disciplines.unable_discipline(id)
    flash("Se cambió el estado de la disciplina", "success")
    return redirect(url_for("disciplines.disciplines_show", page=page))


@disciplines_blueprint.post('/destroy/<int:id>/<int:page>')
@login_required
@permission_required
def disciplines_destroy(id, page):
    """Controlador para eliminar una disciplina"""

    disciplines.destroy_discipline(id)
    flash("Se eliminó la disciplina", "success")
    return redirect(url_for("disciplines.disciplines_show", page=page))


@disciplines_blueprint.post('/desasociate/<int:id_categorie>/<int:id_discipline>')
@login_required
@permission_required
def discipline_desasociate_c(id_categorie, id_discipline):
    """Controlador para quitar una categoría de una disciplina"""

    disciplines.desassociate_discipline_category(id_discipline, id_categorie)
    flash("Se eliminó la categoría de la disciplina", "success")
    return redirect(url_for("disciplines.disciplines_index", id=id_discipline))
