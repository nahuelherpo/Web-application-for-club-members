from datetime import date, datetime

import bcrypt

from src.core.associates.associate import DocumentTypeEnum, GenderEnum
from src.core import auth
from src.core import payments
from src.core import associates
from src.core import adminConfig
from src.core import disciplines


def run():
    """Crea los registros iniciales de las tablas de la BD."""

    passwd = b'hola'
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(passwd, salt)
    hashed = hashed.decode('utf-8')

    default_config = adminConfig.create_config(
        cant_elementos=10,
        pago_habilitado=False,
        info_contacto="Esta es la infor de contacto",
        texto_recibo="Pago aceptado",
        valor_cuota_base=500.0,
        porcentaje_recargo=12,
    )

    permission1_1 = auth.create_permission(
        name="user_index"
    )
    permission1_2 = auth.create_permission(
        name="user_new"
    )
    permission1_3 = auth.create_permission(
        name="user_destroy"
    )
    permission1_4 = auth.create_permission(
        name="user_update"
    )
    permission1_5 = auth.create_permission(
        name="user_show"
    )
    permission1_6 = auth.create_permission(
        name="user_activate"
    )
    permission1_7 = auth.create_permission(
        name="user_deactivate"
    )
    permission1_8 = auth.create_permission(
        name="user_unassign_role"
    )
    permission1_9 = auth.create_permission(
        name="user_assign_role"
    )

    permission2_1 = auth.create_permission(
        name="associates_index"
    )
    permission2_2 = auth.create_permission(
        name="associates_new"
    )
    permission2_3 = auth.create_permission(
        name="associates_destroy"
    )
    permission2_4 = auth.create_permission(
        name="associates_update"
    )
    permission2_5 = auth.create_permission(
        name="associates_show"
    )

    permission2_6 = auth.create_permission(
        name="toggle_status_associate"
    )

    permission3_1 = auth.create_permission(
        name="disciplines_index"
    )
    permission3_2 = auth.create_permission(
        name="disciplines_new"
    )
    permission3_3 = auth.create_permission(
        name="disciplines_destroy"
    )
    permission3_4 = auth.create_permission(
        name="disciplines_update"
    )
    permission3_5 = auth.create_permission(
        name="disciplines_show"
    )
    permission3_6 = auth.create_permission(
        name="discipline_add_categorie"
    )
    permission3_7 = auth.create_permission(
        name="discipline_create_categorie"
    )
    permission3_8 = auth.create_permission(
        name="disciplines_update_enabled"
    )
    permission3_9 = auth.create_permission(
        name="discipline_desasociate_c"
    )

    permission4_1 = auth.create_permission(
        name="inscriptions_show"
    )
    permission4_2 = auth.create_permission(
        name="inscriptions_make"
    )

    permission5_1 = auth.create_permission(
        name="payments_index"
    )
    permission5_2 = auth.create_permission(
        name="payments_show_fees"
    )
    permission5_3 = auth.create_permission(
        name="payments_create_fee"
    )
    permission5_4 = auth.create_permission(
        name="payments_create_fee_receipt"
    )
    permission5_5 = auth.create_permission(
        name="payments_export_fee_receipt"
    )
    permission5_6 = auth.create_permission(
        name="payments_search_associate_fees"
    )

    permission6_1 = auth.create_permission(
        name="config_index"
    )
    permission6_2 = auth.create_permission(
        name="config_update"
    )

    role1 = auth.create_role(
        name="operador",
        permissions=[permission2_1, permission2_2,
                     permission2_4, permission2_5, permission3_1,
                     permission3_2, permission3_4, permission3_5,
                     permission3_6, permission3_7, permission3_8,
                     permission3_9, permission4_1, permission4_2]
    )
    role2 = auth.create_role(
        name="administrador",
        permissions=[permission1_1, permission1_2, permission1_3,
                     permission1_4, permission1_5, permission1_6,
                     permission1_7, permission1_8, permission1_9,
                     permission2_1, permission2_2, permission2_3,
                     permission2_4, permission2_5, permission3_1,
                     permission3_2, permission3_3, permission3_4,
                     permission3_5, permission3_6, permission3_7,
                     permission3_8, permission3_9, permission4_1,
                     permission4_2, permission5_1, permission5_2,
                     permission5_3, permission5_4, permission5_5, permission5_6,
                     permission6_1, permission6_2]
    )

    user1 = auth.create_user(
        username="admin",
        email="admin@admin.com",
        name="admin",
        surname="admin",
        password=hashed,
        active=True,
        roles=[role2]
    )
    user2 = auth.create_user(
        username="Osvaldo03",
        email="laport_osvaldo@hotmail.com",
        name="Osvaldo",
        surname="Laport",
        password=hashed,
        active=True,
        roles=[role2]
    )
    user3 = auth.create_user(
        username="LaTripleT",
        email="tinitinitini@hotmail.com",
        name="Martina",
        surname="Stoessel",
        password=hashed,
        active=True,
        roles=[role1]
    )
    dis = None

    # Creo algunas disciplinas de prueba para agregar a
    # los asociados, de abajo.

    cat1 = disciplines.create_category(
        name="Mini", instructors="Marcos", days="Miercoles y Jueves", hour_fence="9 a 11")
    cat2 = disciplines.create_category(
        name="Juvenil", instructors="Patricia", days="Viernes y Sábados", hour_fence="13 a 15")

    dis = disciplines.create_discipline(
        name="Básquet",
        monthly_price="450",
        enabled=True,
        categories=[cat1, cat2]
    )

    # Creo algunos asociados de prueba.

    associate1 = associates.create_associate(
        name="Maria",
        surname="Gimenez",
        document_type=DocumentTypeEnum.dni,
        document_number=28456851,
        gender=GenderEnum.f,
        address="Calle 7, altura 1700",
        status=True,
        phone_number="+54 221 42568547",
        email="mariagomez@hotmail.com",
        password=hashed,
        date_of_birth=datetime.strptime("10/12/1998","%d/%m/%Y").date()
    )

    # Maria va a deber una cuota del año pasado, sera morosa
    payments.create_fee(
        year=2021,
        month=5,
        paid=False,
        amount_to_pay=100,
        expiration_date=date(2021, 5, 10),
        associate=associate1
    )

    associate2 = associates.create_associate(
        name="Juan Pablo",
        surname="Gimenez",
        document_type=DocumentTypeEnum.dni,
        document_number=26524715,
        gender=GenderEnum.m,
        address="Calle 7, altura 1700",
        status=True,
        phone_number="+54 221 4568521",
        email="juanpagimez@hotmail.com",
        password=hashed,
        date_of_birth=datetime.strptime("26/11/1990","%d/%m/%Y").date(),
        disciplines_practiced=[dis],
    )

    associate3 = associates.create_associate(
        name="Jorge",
        surname="Martinez",
        document_type=DocumentTypeEnum.dni,
        document_number=15412581,
        gender=GenderEnum.m,
        address="Calle 32, altura 4552",
        status=True,
        phone_number="+54 221 4585236",
        email="jorgemarti@yahoo.com",
        password=hashed,
        date_of_birth=datetime.strptime("20/11/1990","%d/%m/%Y").date(),
        disciplines_practiced=[dis],
    )
    receipt1 = payments.create_receipt(
        paid_by="Sergio Gomez",
        amount_paid=1000,
        payment_date=date(2022, 4, 3)
    )
    fee1 = payments.create_fee(
        year=2022,
        month=4,
        paid=True,
        associate_id=1,
        associate=associate1,
        amount_to_pay=100,
        expiration_date=date(2022, 4, 10),
        receipt=receipt1
    )

    fee2 = payments.create_fee(
        year=2022,
        month=5,
        paid=False,
        associate_id=1,
        associate=associate1,
        amount_to_pay=100,
        expiration_date=date(2022, 5, 10),
        receipt=None
    )

    fee3 = payments.create_fee(
        year=2022,
        month=6,
        paid=False,
        associate_id=1,
        associate=associate1,
        amount_to_pay=100,
        expiration_date=date(2022, 6, 10),
        receipt=None
    )
