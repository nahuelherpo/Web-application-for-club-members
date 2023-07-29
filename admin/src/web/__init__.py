from datetime import timedelta

from flask import Flask
from flask import session
from flask import render_template
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.core import database
from src.core import seeds
from src.web.config import config
from src.web.helpers import handlers
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.config import config_blueprint
from src.web.controllers.users import users_blueprint
from src.web.controllers.payments import payments_blueprint
from src.web.controllers.associates import associates_blueprint
from src.web.controllers.disciplines import disciplines_blueprint
from src.web.controllers.api import ListClubDisciplines
from src.web.controllers.api import ListMyPayments
from src.web.controllers.api import ListMyDisciplines
from src.web.controllers.api import Profile
from src.web.controllers.api import Login
from src.web.controllers.api import Logout
from src.web.controllers.api import EstadisticasAsociadosPorGenero
from src.web.controllers.api import EstadisticasDisciplinasPorEdad
from src.web.controllers.api import EstadisticasAsociadosActivosNoActivos
from src.web.controllers.api import ListAllDisciplines
from src.web.controllers.api import MiCarnet
from src.web.controllers.api import StatsDiscipline
from src.web.controllers.api import ClubInfo
from src.web.controllers.inscriptions import inscriptions_blueprint
import os


def create_app(env="development", static_folder="static"):

    app = Flask(__name__, static_folder=static_folder)

    cors = CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_object(config[env])

    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    jwt = JWTManager(app)

    api = Api(app)

    database.init_app(app)

    @app.get('/')
    def home():
        # database.reset_db()
        # seeds.run()
        return render_template('layout.html', logged=True)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(config_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(payments_blueprint)
    app.register_blueprint(associates_blueprint)
    app.register_blueprint(inscriptions_blueprint)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.generic_error)
    app.register_error_handler(401, handlers.unauthorized_error)

    # app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.register_blueprint(disciplines_blueprint)

    # app.jinja.env.globals.update(is_authenticated=auth.is_authenticated)

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    api.add_resource(ListClubDisciplines, '/api/club/disciplines')
    api.add_resource(ListMyDisciplines, '/api/me/disciplines')
    api.add_resource(ListMyPayments, '/api/me/payments')
    api.add_resource(Login, '/api/auth')
    api.add_resource(Profile, '/api/me/profile')
    api.add_resource(Logout, '/api/logout')
    api.add_resource(MiCarnet, '/api/me/license')
    api.add_resource(EstadisticasAsociadosPorGenero, '/api/statsgenere')
    api.add_resource(EstadisticasDisciplinasPorEdad, '/api/statsage')
    api.add_resource(EstadisticasAsociadosActivosNoActivos, '/api/actives')
    api.add_resource(ListAllDisciplines, '/api/allDisciplines')
    api.add_resource(StatsDiscipline, '/api/statsdiscipline')
    api.add_resource(ClubInfo, '/api/club/info')
    return app
