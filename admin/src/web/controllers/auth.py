from flask import Blueprint
from flask import flash
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from src.web.helpers.auth import login_required
from src.core import auth


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    """Devuelve la página de login."""

    if ('logged' in session and session['logged']):
        return redirect(url_for("home"))
    return render_template("auth/login.html")


@auth_blueprint.post("/authenticate")
def authenticate():
    """El método recibe los parametros del form, busca si hay algun usuario en la BD que correspondan a eso
    datos, en caso de no corresponder devuelve al usuario a la pantalla de login con un mensaje de error
    y en caso de corresponder le da acceso al sistema"""

    params = request.form
    user = auth.find_user_by_mail_or_username_and_pass(
        params["email"].lower(), params["password"])
    if not user:
        flash("Email o contraseña inválidos", "danger")
        return redirect(url_for("auth.login"))
    if (not user.active):
        flash("Su usuario esta inhabilitado. Por favor, comuníquese con admin@clubsis.com", "danger")
        return redirect(url_for("auth.login"))
    roles = []
    for rol in user.roles:
        roles.append(rol.name)

    session["logged"] = True
    session["user"] = {"id": user.id, "email": user.email.lower(), "username": user.username,
                       "name": user.name, "roles":  roles}

    flash("La sesión ha sido iniciada correctamente", "success")

    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
@login_required
def logout():
    """Cierra la sesión del usuario."""

    if (session["logged"] == True):
        del session["user"]
    session.clear()
    session["logged"] = False
    flash("la sesión se ha cerrado correctamente", "success")

    return redirect(url_for("auth.login"))
