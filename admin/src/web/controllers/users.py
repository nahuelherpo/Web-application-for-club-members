import math

import bcrypt
from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import session
from flask import url_for
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms import PasswordField

from src.core import auth
from src.core import adminConfig
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.core.auth import find_user_by_mail_or_username


users_blueprint = Blueprint('user', __name__, url_prefix='/users')


class UserEditForm(FlaskForm):
    """Formulario de edición de un usuario"""

    username = TextAreaField('Nombre de usuario:', validators=[
                             DataRequired(), Length(4, 32)], render_kw={"rows": 2, "cols": 2})
    email = TextAreaField('Correo:', validators=[DataRequired(), Length(
        5, 255)], render_kw={"rows": 2, "cols": 2})
    name = TextAreaField('Nombre:', validators=[DataRequired(), Length(
        4, 32)], render_kw={"rows": 2, "cols": 2})
    surname = TextAreaField('Apellido:', validators=[
                            DataRequired(), Length(4, 32)], render_kw={"rows": 2, "cols": 2})


class UserNewForm(FlaskForm):
    """Formulario de creación de un usuario"""

    username = TextAreaField('Nombre de usuario:', validators=[
                             DataRequired(), Length(4, 32)], render_kw={"rows": 2, "cols": 2})
    email = EmailField('Correo:', validators=[DataRequired(), Length(
        5, 255)], render_kw={"rows": 2, "cols": 2})
    name = TextAreaField('Nombre:', validators=[DataRequired(), Length(
        4, 32)], render_kw={"rows": 2, "cols": 2})
    surname = TextAreaField('Apellido:', validators=[
                            DataRequired(), Length(4, 32)], render_kw={"rows": 2, "cols": 2})
    password = PasswordField('Contraseña:', validators=[
                             DataRequired(), Length(8, 32)], render_kw={"rows": 2, "cols": 2})


@users_blueprint.get('/<int:page>')
@login_required
@permission_required
def user_index(page):
    """Esta funcion nos lleva a la lista de usuarios del sistema
    -page: indica la pagina del listado, la cant.  de  elementos
    por pagina estan establecidos en la config. del sistema."""

    if (page < 1):
        flash("La página solicitada no existe", "danger")
        return user_index(1)

    users = auth.users_paged_list(page)
    nums = math.ceil(len(list(auth.list_users())) /
                     (adminConfig.list_config()).cant_elementos)

    if (page > nums):
        flash("La página solicitada no existe", "danger")

    return render_template('users/users_list.html/', page=page, nums=nums, users=users, filter=False)


@users_blueprint.get('/filter')
@login_required
def user_filtered_index():
    """Esta función nos lleva a una versión del index filtrada por
    parametros que le llegan mediando el metodo GET"""

    params = request.args
    page = int(params['page'])
    email = params['email']
    state = params['state']

    if email == '' and state == '':
        return redirect(url_for("user.user_index", page=1))

    if email == '':
        amount, user = auth.list_users_filter_by_status(page, state)
    elif state == '':
        amount, user = auth.list_users_filter_by_email(page, email)
    else:
        amount, user = auth.list_users_filter_by_email_and_status(
            page, email, state)

    config = adminConfig.list_config()
    nums = math.ceil(amount/config.cant_elementos)

    if (len(user) < 1):
        flash("No se han encontrado usuarios con los atributos especificados", 'warning')

    return render_template('users/users_list.html', users=user, nums=nums, page=int(page), email=email, state=state, filter=True)


@users_blueprint.get('/edit/<int:id>')
@login_required
@permission_required
def user_update(id):
    """Editar los atributos de un usuario"""

    user = auth.get_user_by_id(id)
    form = UserEditForm(
        username=user.username,
        email=user.email,
        name=user.name,
        surname=user.surname
    )
    return render_template('users/edit_user.html', user=user, form=form)


@users_blueprint.post('/activate')
@login_required
@permission_required
def user_activate():
    """Pasa el estado de un usuario a activo. Si ya estuviese activo, no hace nada."""

    data = request.form
    user = auth.get_user_by_id(data["user_id"])
    auth.activate_user(user)
    flash("El usuario fue habilitado con éxito", "success")

    return redirect(url_for("user.user_index", page=1))


@users_blueprint.post('/deactivate')
@login_required
@permission_required
def user_deactivate():
    """Pasa el estado de un usuario a inactivo. Si ya estuviese inactivo, no hace nada."""

    data = request.form
    user = auth.get_user_by_id(data["user_id"])
    if user and user.active:
        if (session["user"]["id"] == user.id):
            flash("No puede deshabilitarse a sí mismo", "warning")
        else:
            auth.deactivate_user(user)
            flash("El usuario fue deshabilitado con éxito", "success")
    else:
        flash("El usuario especificado no existe", "danger")
    return redirect(url_for("user.user_index", page=1))


@users_blueprint.post('/assign_role')
@login_required
@permission_required
def user_assign_role():
    """Le asigna el rol especificado al usuario."""

    data = request.form
    user = auth.get_user_by_id(data["user_id"])
    role = auth.find_role_by_name(data["role_name"])
    if role in user.roles:
        flash(
            f"El usuario {user.username} ya posee el rol {role.name}", "warning")
        return redirect(url_for("user.user_index", page=1))

    if user and role:
        auth.assign_role(user, role)
        flash(
            f"El rol {role.name} ha sido asignado correctamente al usuario {user.username}", 'success')
    else:
        flash("El usuario o rol especificado no existen", "danger")

    return redirect(url_for("user.user_index", page=1))


@users_blueprint.post('/unassign_role')
@login_required
@permission_required
def user_unassign_role():
    """Le desasigna el rol especificado al usuario."""

    data = request.form
    if (int(data["user_id"]) == session["user"]["id"]) and (data["role_name"] == "administrador"):
        flash("No puede quitarse el rol de administrador a si mismo", "danger")
    else:
        user = auth.get_user_by_id(data["user_id"])
        role = auth.find_role_by_name(data["role_name"])
        if role not in user.roles:
            flash(
                f"El usuario {user.username} no posee el rol {role.name}", "warning")
            return redirect(url_for("user.user_index", page=1))
        if user and role:
            auth.unassign_role(user, role)
            flash(
                f"El rol {role.name} ha sido quitado correctamente al usuario {user.username}", 'success')
        else:
            flash("El usuario o rol especificado no existen", "danger")

    return redirect(url_for("user.user_index", page=1))


@users_blueprint.post('/edit/<int:id>')
@login_required
def edit_user(id):
    """Este método captura los campos del formulario, los validad
    y si son correctos actualiza la entidad de interes.       """

    form = UserEditForm(request.form)
    if (form.validate()):
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        user_aux_username = auth.find_user_by_mail_or_username(username)
        user_aux_email = auth.find_user_by_mail_or_username(email)
        if user_aux_username != None and user_aux_username.id != id:
            flash(
                "Ya existe un usuario con el mismo nombre de usuario, ingrese otro", "danger")
        elif user_aux_email != None and user_aux_email.id != id:
            flash("Ya existe un usuario con el mismo correo, ingrese otro", "danger")
        else:
            name = request.form.get('name')
            surname = request.form.get('surname')
            auth.update_user(id, username, email, name.strip(), surname.strip())
            flash("Usuario actualizado con éxito", "success")
    else:
        flash("Ocurrió un error al validar los campos, inténtelo nuevamente", "danger")

    return redirect(url_for('user.user_index', page=1))


@users_blueprint.get('/new/')
@login_required
@permission_required
def user_new():
    """En esta pantalla se levanta el form, para ingresar
    los campos del usuario a crear."""

    form = UserNewForm()

    return render_template('users/new_user.html', form=form)


@users_blueprint.post('/new/')
@login_required
def create_new_user():
    """Esta funcion es la que crea el nuevo usuario
    tomando los campos ingresador en el form."""

    form = UserNewForm(request.form)
    print(request.form)
    if (form.validate()):
        # Tomo los valores del formulario
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        name = request.form.get('name').strip()
        surname = request.form.get('surname').strip()
        passwd = request.form.get('password').strip()

        # Chequeo si no existe otro usuario con el mismo username o email
        if auth.find_user_by_mail_or_username(username) != None:
            flash(
                "Ya existe un usuario con el mismo nombre de usuario, ingrese otro", "danger")
        elif auth.find_user_by_mail_or_username(email) != None:
            flash("Ya existe un usuario con el mismo correo, ingrese otro", "danger")
        else:
            # Creo el usuario
            auth.create_user(
                username=username,
                email=email,
                name=name,
                surname=surname,
                password=(bcrypt.hashpw(str.encode(passwd),
                                        bcrypt.gensalt(12))).decode('utf-8'),
                active=True)
            flash("Usuario creado con éxito", "success")
    else:
        flash("Ocurrió un error al validar los campos, inténtelo nuevamente", "danger")

    return redirect(url_for('user.user_index', page=1))


@users_blueprint.post('/delete/<int:id>')
@login_required
@permission_required
def user_destroy(id):
    """Esta funcion elimina al usuario con el id pasado por parametro
    -id: id del usuario a eliminar."""

    user = find_user_by_mail_or_username(session['user']['email'])
    if user.id != id:
        auth.delete_user_by_id(id)
        flash("Usuario eliminado con éxito", "success")
    else:
        flash("No puede eliminarse a si mismo", "danger")

    return redirect(url_for('user.user_index', page=1))
