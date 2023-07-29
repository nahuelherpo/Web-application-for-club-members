from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    """Inicia y configura inicialment a la BD"""

    db.init_app(app)
    config_db(app)


def config_db(app):
    """Crea todas las tablas que estan mapeadas
    con el ORM."""

    @app.before_first_request
    def init_database():
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    """Resetea la BD"""

    print("eliminando base de datos")
    db.drop_all()
    print("creando base de datos")
    db.create_all()
    print("base de datos lista")
