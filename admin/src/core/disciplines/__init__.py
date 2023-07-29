import math

from src.core.associates.discipline import Discipline
from src.core.associates.category import Category
from src.core.database import db
from src.core.adminConfig import list_config


def get_discipline_by_id(id):
    """Este metodo devuelve la disciplina con id pasado por parametro"""

    return Discipline.query.filter_by(id=id).first()


def list_all_disciplines():
    """Este metodo devuelve todas las disciplinas que posee el club."""

    return Discipline.query.all()


def list_all_enabled_disciplines():
    """Este metodo devuelve todas las disciplinas habilitadas que posee el club."""

    return Discipline.query.filter_by(enabled=True).all()


def list_disciplines(page):
    """Trae los elementos dependiendo de la pagina en la que se encuentre."""
    config = list_config().cant_elementos
    ele = Discipline.query.order_by(Discipline.id.asc()).filter().limit(
        config).offset((page - 1) * config).all()
    return ele


def paginated_quantity_discipline():
    """Calcula cuantas paginas tiene que crear la vista"""

    config = list_config()
    return math.ceil(Discipline.query.count()/config.cant_elementos)


def create_discipline(**kwargs):
    """Crea una disciplinas con los parametros de entrada y la retorna"""

    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()
    return discipline


def create_category(**kwargs):
    """Crea una categoría con los parametros de entrada y la retorna"""

    category = Category(**kwargs)
    db.session.add(category)
    db.session.commit()
    return category


def detail_discipline(id: int):
    """Devuelve la disciplina y las lista de categorías del id de la disciplina que se pasa por parámetro,
    en caso de que no exista retorna None y una lista vacía."""

    dis_selected = Discipline.query.get(id)
    categories = None
    if (dis_selected):
        categories = dis_selected.categories
    return dis_selected, categories


def list_categories():
    """Retorna una lista con todas las categorías."""

    return Category.query.all()


def detail_category(id: int):
    """Retorna la categoría correspondiente al id pasado por parámetro, si no existe,
    retorna None."""

    return Category.query.get(id)


def create_and_add_category(name, instructors, days, hour_fence, id):
    """Crea una nueva categoría con los parámetros pasados y se la asigna a la
    disciplina con el id detallado."""

    new_category = Category(
        name=name, instructors=instructors, days=days, hour_fence=hour_fence)
    db.session.add(new_category)
    db.session.commit()
    dis_selected = Discipline.query.get(id)
    dis_selected.categories.append(new_category)
    db.session.add(dis_selected)
    db.session.commit()
    return dis_selected


def add_category(id_discipline: int, id_category: int):
    """Agrega una categoría a una disciplina pero primero comprueba que ya no exista"""

    category = detail_category(id_category)
    dis = Discipline.query.get(id_discipline)
    if (check_category_exist(dis, id_category)):
        return True
    dis.categories.append(category)
    db.session.add(dis)
    db.session.commit()
    return False


def check_category_exist(dis, id_category):
    """Chequea si la categoría pertenece a la lista de categorías de la disciplina"""

    for categories in dis.categories:
        if (categories.id == id_category):
            return True
    return False


def edit_discipline(id_discipline: int, new_name, new_price):
    """Modifica una disciplina"""

    new_dis = Discipline.query.filter_by(id=id_discipline).update(
        dict(name=new_name, monthly_price=new_price))
    db.session.commit()
    return new_dis


def unable_discipline(id_discipline: int):
    """Deshabilita/Habilita una disciplina"""

    new_dis = Discipline.query.get(id_discipline)
    new_dis.enabled = not new_dis.enabled
    db.session.commit()
    return new_dis


def destroy_discipline(id_discipline: int):
    """Borra una disciplina"""

    dis_destroyed = Discipline.query.filter_by(id=id_discipline).one()
    db.session.delete(dis_destroyed)
    db.session.commit()
    return dis_destroyed


def desassociate_discipline_category(id_discipline: int, id_category: int):
    """Elimina una categoría de una disciplina"""

    new_categories = []
    dis_desassociate = Discipline.query.filter_by(id=id_discipline).one()
    for category in dis_desassociate.categories:
        if (category.id != id_category):
            new_categories.append(category)
    dis_desassociate.categories = new_categories
    db.session.commit()
    return dis_desassociate
