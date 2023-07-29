from src.core.adminConfig.config import Config

from src.core.database import db


def list_config():
    """Retorna la configuracion del sistema, si no existe nada con el id 1
    la crea y luego la retorna"""

    configuration = Config.query.get(1)
    if (configuration is None):
        config = create_config(
            id=1,
            cant_elementos=10,
            pago_habilitado=True,
            info_contacto="Informacion de contacto por defecto",
            texto_recibo="Pago aceptado",
            valor_cuota_base=200,
            porcentaje_recargo=10,
        )
        return config
    else:
        return configuration


def update_config(cant_elementos=10, pago_habilitado=True,
                  info_contacto="Informacion de contacto por defecto",
                  texto_recibo="Pago aceptado",
                  valor_cuota_base=200,
                  porcentaje_recargo=10):
    """Recibe los valores modificados para la configuracion y los guarda."""

    nueva_config = list_config()
    nueva_config.cant_elementos = cant_elementos
    nueva_config.pago_habilitado = pago_habilitado
    nueva_config.info_contacto = info_contacto
    nueva_config.texto_recibo = texto_recibo
    nueva_config.valor_cuota_base = valor_cuota_base
    nueva_config.porcentaje_recargo = porcentaje_recargo
    db.session.commit()
    return nueva_config


def create_config(**kwargs):
    """Crea la configuración solo si no existe una actualmente, sino retorna None."""

    if (Config.query.count() == 0):
        config = Config(**kwargs)
        db.session.add(config)
        db.session.commit()
        return config
    else:
        return None
