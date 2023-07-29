import bcrypt
import pandas as pd

from src.core.associates.associate import Associate
from src.core.associates.category import Category
from src.core.associates.discipline import Discipline
from src.web.helpers.auxiliar_functions import calculate_age
from src.core.database import db
from src.core.adminConfig import list_config


def find_associate_by_dni(dni):
    """Retorna el asociado con dni 'document_number' en caso de que exista, cc retorna None"""

    return Associate.query.filter_by(document_number=dni).first()


def find_associate_by_dni_and_pass(dni, password):
    """Este metodo primero busca en la base de datos un dni igual al dni que llega por parametro, si existe, se fija
    si la contraseña hasheada que tiene asociada al dni coincide con la ingresa por el usuario, devuelve el usuario, sino
    devuelve None"""

    user = Associate.query.filter_by(document_number=dni).first()

    if user:
        hashed = str.encode(password)
        hashedpass = str.encode(user.password)
        if bcrypt.checkpw(hashed, hashedpass):
            return user

    return None


def list_all_associates():
    """Esta funcion retorna todos los asociados en la base de datos"""

    return Associate.query.filter(~Associate.name.startswith("*")).order_by(Associate.id).all()


def list_all_associates_filter_by_status(status):
    """Esta funcion retorna todos los asociados en la base de datos
    con el estado igual al estado que llega como parametro"""

    return Associate.query.filter_by(status=status).filter(~Associate.name.startswith("*")).order_by(Associate.id).all()


def list_all_associates_filter_by_surname_and_status(surname, status):
    """Esta funcion retorna todos los asociados en la base de datos
    con el email que contenga al parametro 'email' y tenga el mismo estado
    que el estado que llega como parametro """

    return Associate.query.filter((Associate.surname.contains(surname)) & (Associate.status == status)).filter(~Associate.name.startswith("*")).order_by(Associate.id).all()


def list_all_associates_filter_by_surname(surname: str):
    """Esta función retorna todos los asociados en la base de datos
    con el apellido que contenga el parámetro surname"""

    return Associate.query.filter(Associate.surname.contains(surname)).filter(~Associate.name.startswith("*")).all()


def count_all_associates_filter_by_genere_masculine():
    """Esta función retorna la cantidad de asociados masculinos en el sistema"""

    return Associate.query.filter(~Associate.name.startswith("*")).filter_by(gender="m").count()


def count_all_associates_filter_by_genere_femenine():
    """Esta función retorna la cantidad de asociados femeninos en el sistema"""

    return Associate.query.filter(~Associate.name.startswith("*")).filter_by(gender="f").count()


def count_all_associates_filter_by_genere_other():
    """Esta función retorna la cantidad de asociados femeninos en el sistema"""

    return Associate.query.filter(~Associate.name.startswith("*")).filter_by(gender="otro").count()


def count_all_asociates_by_age():
    """Esta función retorna la cantidad de asociados por edad en el sistema"""
    assoc = Associate.query.filter(~Associate.name.startswith("*")).with_entities(
        Associate.id, Associate.date_of_birth).all()
    assoc_df = pd.DataFrame([(a.id, a.date_of_birth)
                            for a in assoc], columns=["id", "date_of_birth"])
    assoc_df = assoc_df.drop("id", axis=1)
    assoc_df = assoc_df.applymap(calculate_age)
    assoc_df = assoc_df.groupby("date_of_birth").value_counts().to_dict()
    ages = [0] * 100
    for key, value in assoc_df.items():
        ages[key] = value
    return ages


def list_associates(page):
    """"Devuelve una lista de una fraccion de los asociados limitando
    la cantidad por la paginacion de la configuracion, tambien devuelve
    la cantidad de asociados total"""

    config = list_config().cant_elementos
    aux = Associate.query.filter(
        ~Associate.name.startswith("*")).order_by(Associate.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1)*config).all()
    return (amount, assoc)


def list_associates_filter_by_surname(page, surname):
    """Esta funcion devuelve una lista de una fraccion de los asociados
    con el email que contenga al parametro 'surname' y limitando la cantidad 
    por la paginacion de la configuracion, tambien devuelve la cantidad de
    asociados con esas caracteristicas"""

    config = list_config().cant_elementos

    aux = Associate.query.filter(Associate.surname.contains(surname)).filter(
        ~Associate.name.startswith("*")).order_by(Associate.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()

    return (amount, assoc)


def list_associates_filter_by_status(page, status):
    """Esta funcion devuelve una lista de una fraccion de los asociados
    con el estado igual al estado que llega por parametro y limitando la cantidad
    por la paginacion de la configuracion, tambien devuelve la cantidad de asociados
    con esas caracteristicas"""

    config = list_config().cant_elementos

    aux = Associate.query.filter_by(status=status).filter(
        ~Associate.name.startswith("*")).order_by(Associate.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()
    return (amount, assoc)


def list_associates_filter_by_surname_and_status(page, surname, status):
    """Esta funcion devuelve una lista de una fraccion de los asociados
    con el email contenido en el parametro 'email', con el estado igual al
    estado que llega por parametro y limitando la cantidad por la paginacion
    de la configuracion, tambien devuelve la cantidad de los asociados con esas caracteristicas"""

    config = list_config().cant_elementos
    aux = Associate.query.filter((Associate.surname.contains(surname)) & (
        Associate.status == status)).filter(~Associate.name.startswith("*")).order_by(Associate.id)
    amount = aux.count()
    assoc = aux.limit(
        config).offset((page - 1) * config).all()
    return (amount, assoc)


def create_associate(**kwargs):
    """Crea un asociado con los parámetros enviados:
    -name: nombre del asociado
    -surname: apellido del asociado
    -document_type: tipo de documento, recibe DocumentTypeEnum 
    -document_number: número de documento (String)
    -gender: género, recibe GenderEnum
    -address: dirección del asociado
    -status: estatus (por defecto activo)
    -phone_number: teléfono del asociado (opcional)
    -email: email del asociado (opcional)
    -password: contraseña del asociado encriptada
    -fees: lista de cuotas perteneciente al asociado (opcional)
    -disciplines_practiced = lista de disciplinas que practica el asociado (opcional)"""

    associate = Associate(**kwargs)
    db.session.add(associate)
    db.session.commit()

    return associate


def update_associate(id, surname, email, name, phone_number, address, gender, document_number, document_type):
    """Este metodo busca un asociado en la base de datos por su id 
    y le actualiza sus datos, luego lo retorna"""

    associ = Associate.query.get(id)
    associ.name = name
    associ.surname = surname
    associ.document_type = document_type
    associ.document_number = document_number
    associ.gender = gender
    associ.address = address
    associ.phone_number = phone_number
    associ.email = email
    db.session.commit()
    return associ


def update_status(status, id):
    """Esta funcion actualiza unicamente el estado de un asociado
    con el id igual al 'id' que se le envia como parametro"""

    associ = Associate.query.get(id)
    associ.status = status
    db.session.commit()
    return associ


def delete_associate_by_id(id):
    """Este metodo busca un asociado en la base de datos por su id y lo elimina"""

    associ = Associate.query.get(id)
    associ.name = '*' + associ.name
    db.session.commit()
    return associ


def get_associate_by_id(id):
    """Este metodo le llega un id y devuelve el asociado al que le pertenece ese id"""

    return Associate.query.get(id)


def list_categories():
    """"Devuelve una lista de todas las categorías"""

    return Category.query.all()


def create_category(**kwargs):
    """Crea una categoría con los parámetros enviados:
    -name: nombre de la categoría
    -instructors: nombres de instructores
    -days: días en que se practica (String)
    -hour_fence: horario en que se practica (String)"""

    category = Category(**kwargs)
    db.session.add(category)
    db.session.commit()

    return category


def list_disciplines():
    """"Devuelve una lista de todas las disciplinas"""

    return Discipline.query.all()


def create_discipline(**kwargs):
    """Crea una disciplina con los parámetros enviados:
    -name: nombre de la disciplina
    -monthly_price: precio por mes
    -enabled: habilitada/deshabilitada (Por defecto esta habilitada)
    -categories: lista de categorías de la disciplina (opcional)"""

    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()

    return discipline


def get_discipline_by_id(id):
    """Retorna la disciplina con el id pasado por parámetro."""

    return Discipline.query.get(id)


def create_inscription(id_associate, id_discipline):
    """Le asigna la disciplina con id id_discipline al asociado con
    id id_associate"""

    associate = get_associate_by_id(id_associate)
    discipline = get_discipline_by_id(id_discipline)
    if (not discipline or not associate):
        return False
    if discipline in associate.disciplines_practiced:
        return False
    associate.disciplines_practiced.append(discipline)
    db.session.commit()
    return True


def list_active_associates():
    """Retorna una lista de todos los asociados activos."""

    return Associate.query.filter_by(status=True).filter(~Associate.name.startswith("*")).all()


def update_card_date(id, today):
    """Esta funcion actualiza el valor de la fecha de emision del carnet"""

    assoc = Associate.query.get(id)
    assoc.card_issue_date = today
    db.session.commit()

    return True
