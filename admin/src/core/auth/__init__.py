import bcrypt

from src.core.auth.user import User
from src.core.auth.permission import Permission
from src.core.auth.role import Role
from src.core.database import db
from src.core import adminConfig


def list_users():
    """"Devuelve una lista de todos los usuarios"""

    return User.query.all()


def users_paged_list(page):
    """Devuelve los usuarios correspondientes al número de página enviado por parámetro."""

    config = (adminConfig.list_config()).cant_elementos
    users_page = User.query.order_by(User.id.asc()).filter().limit(
        config).offset((page - 1) * config).all()
    return users_page


def list_users_filter_by_email(page, email):
    """Esta funcion devuelve una lista de una fraccion de los usuarios
    con el email que contenga al parametro 'email' y limitando la cantidad 
    por la paginacion de la configuracion, tambien devuelve la cantidad de
    usuarios con esas caracteristicas."""

    config = adminConfig.list_config().cant_elementos

    aux = User.query.filter(User.email.contains(email)).order_by(User.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()

    return (amount, assoc)


def list_users_filter_by_status(page, status):
    """Esta funcion devuelve una lista de una fraccion de los usuarios
    con el estado igual al estado que llega por parametro y limitando la cantidad
    por la paginación de la configuración, tambien devuelve la cantidad de usuarios
    con esas caracteristicas."""

    config = adminConfig.list_config().cant_elementos

    aux = User.query.filter(User.active == status).order_by(User.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()
    return (amount, assoc)


def list_users_filter_by_email_and_status(page, email, status):
    """Esta funcion devuelve una lista de una fraccion de los asociados
    con el email contenido en el parametro 'email', con el estado igual al
    estado que llega por parametro y limitando la cantidad por la paginacion
    de la configuracion, tambien devuelve la cantidad de los asociados con esas caracteristicas"""

    config = adminConfig.list_config().cant_elementos
    aux = User.query.filter((User.email.contains(email)) & (
        User.active == status)).order_by(User.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()
    return (amount, assoc)


def create_user(**kwargs):
    """Crea un usuario con los parámetros enviados:
    -email: email del usuario (único)
    -username: nickname del usuario (único)
    -name: nombre del usuario
    -surname: apellido del usuario
    -password: contraseña del usuario encriptada
    -active: estatus del usuario
    -roles: lista de roles del usuario (opcional)"""

    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(id):
    """Este metodo devuelve un usuario en base a su id"""

    user = User.query.get(id)
    return user


def update_user(id, username, email, name, surname):
    """Este metodo busca un usuario por su id y 
    actualiza sus campos."""

    user = User.query.get(id)
    user.username = username
    user.email = email
    user.name = name
    user.surname = surname
    db.session.commit()
    return user


def delete_user_by_id(id):
    """Elimina el usuario permanentemente."""

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user


def find_user_by_mail_or_username(name):
    """Busca un usuario en la base de datos, buscando con el parametro de entrada ya sea un mail o un username"""

    return User.query.filter((User.email == name) | (User.username == name)).first()


def find_user_by_mail_or_username_and_pass(name, password):
    """este metodo primero busca en la base de datos un mail igual al mail que llega por parametro, si existe, se fija
    si la contraseña hasheada que tiene asociada al mail coincide con la ingresa por el usuario, devuelve el usuario, sino
    devuelve None"""

    user = find_user_by_mail_or_username(name)

    if user:
        hashed = str.encode(password)
        hashedpass = str.encode(user.password)
        if bcrypt.checkpw(hashed, hashedpass):
            return user

    return None


def assign_role(user: User, role: Role):
    """Asigna el rol indicado al usuario"""

    user.roles.append(role)
    db.session.commit()

    return user


def unassign_role(user: User, role: Role):
    """Quita el rol indicado al usuario"""

    user.roles.remove(role)
    db.session.commit()

    return user


def activate_user(user: User):
    """Activa al usuario pasado por parámetro"""

    user.active = True
    db.session.commit()

    return user


def deactivate_user(user: User):
    """Desactiva al usuario pasado por parámetro"""

    user.active = False
    db.session.commit()

    return user


def list_permissions():
    """"Devuelve una lista de todos los permisos"""

    return Permission.query.all()


def create_permission(**kwargs):
    """Crea un permiso con los parámetros enviados:
    -name: nombre del permiso"""

    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission


def get_permission_by_name(perm):
    """Esta funcion recibe el nombre de un permiso, lo busca en la base de datos y lo devuelvo en caso
    de existir."""

    return Permission.query.filter_by(name=perm).first()


def list_roles():
    """"Devuelve una lista de todos los roles"""

    return Role.query.all()


def create_role(**kwargs):
    """Crea un rol con los parámetros enviados:
    -name: nombre del rol
    -permissions: lista de permisos del rol (opcional)"""

    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def find_role_by_name(name):
    """Busca y retorna el rol con el nombre especificado por parametro, si no lo encuentra,
    devuelve None."""

    return Role.query.filter_by(name=name).first()
