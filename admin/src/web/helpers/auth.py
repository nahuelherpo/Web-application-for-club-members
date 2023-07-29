from functools import wraps

from flask import redirect
from flask import url_for
from flask import session


def is_authenticated(session):
    """Este metodo devuelve si el usuario se encuentra autenticado"""

    return session.get("user") != None


def login_required(f):
    """Funcion decoradora que valida que el usuario este logeado para acceder 
    a la funcion contenida. En caso de que no lo esté, lo redirige a la pantalla
    de login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function
