from src.core.payments.receipt import Receipt
from src.core.payments.fee import Fee
from src.core.database import db
from src.core import adminConfig


def list_fees():
    """"Devuelve una lista de todas las cuotas"""

    return Fee.query.all()


def get_fee_by_id(id):
    """"Devuelve la cuota con el id indicado."""

    return Fee.query.filter_by(id=id).first()


def pay_fee(id):
    """Este metodo registra una cuota como paga.
    -id: id de la cuota"""

    fee = Fee.query.filter_by(id=id).first()
    fee.paid = True

    db.session.commit()

    return fee


def pay_fee_and_assign_receipt(fee, receipt):
    """Esta funcion recibe una cuota y un recibo, marca la couta como paga
    y le asigna el recibo a la couta, luego devuelve la couta."""

    fee.paid = True
    fee.receipt = receipt

    db.session.commit()

    return fee


def update_fee_amount(fee, amount):
    """Recibe una cuota y le modifica la cantidad a pagar"""

    fee.amount_to_pay = amount
    db.session.commit()

    return fee


def create_fee(**kwargs):
    """Crea una cuota con los parámetros enviados:
    -year: año correspondiente a la cuota
    -month: mes correspondiente a la cuota
    -paid: si fue pagado o no (por defecto False)
    -expiration_date: recibe tipo Fecha con la fecha de expiración de la cuota
    -receipt: recibo correspondiente (opcional)"""

    fee = Fee(**kwargs)
    db.session.add(fee)
    db.session.commit()

    return fee


def get_fees_by_associate_id(id):
    """Devuelve las cuotas del asociado pasado por parámetro."""

    fees = Fee.query.filter_by(associate_id=id).all()

    return fees


def get_fees_by_associate_id_paged(id, page):
    """Devuelve las cuotas  para  el  asociado
    con el id pasado, dependiendo de la pagina
    devuelve una cierta cantidad."""

    config = (adminConfig.list_config()).cant_elementos
    fees = Fee.query.order_by(Fee.id.asc()).filter_by(
        associate_id=id).limit(config).offset((page - 1) * config).all()

    return fees


def list_receipts():
    """"Devuelve una lista de todos los recibos"""

    return Receipt.query.all()


def create_receipt(**kwargs):
    """Crea un recibo con los parámetros enviados:
    -payment_date: fecha de pago de la cuota
    -amount_paid: cantidad abonada 
    -paid_by: quién realizó el pago (String)
    -fee: cuota a la que corresponde el recibo"""

    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()

    return receipt
