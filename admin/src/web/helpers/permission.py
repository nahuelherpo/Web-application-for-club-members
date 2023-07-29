from functools import wraps
from flask import session
from flask_restful import abort

from src.core.auth import get_permission_by_name
from src.core.auth import find_user_by_mail_or_username


def permission_required(f):
    """Funcion decoradora que valida que el usuario tenga permisos para acceder 
    a la funcion contenida. En caso de que no lo esté, lo redirige a la pantalla
    de home"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        perm = get_permission_by_name(f.__name__)
        user = session.get("user")["email"]
        user = find_user_by_mail_or_username(user)
        allowed = False
        if user and user.roles != []:
            user_roles = user.roles
            for rol in user_roles:
                if perm in rol.permissions:
                    allowed = True

        if allowed:
            return f(*args, **kwargs)
        abort(401)

    return decorated_function
