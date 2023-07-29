from datetime import datetime
from datetime import date
from pathlib import Path

from flask import jsonify, request
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from src.core import disciplines, payments, associates
from src.core import adminConfig
from datetime import datetime

import base64

dict_status = {"OK": "El socio no registra deuda ni sanción.",
               "Inhabilitado": "El socio posee una sanción.",
               "Deudor": "El socio registra deuda.",
               "Inhabilitado y deudor": "El socio registra deuda y sanción."}


class DisciplineObj(object):
    """Clase que define el objeto disciplina devuelto por la API con los campos correspondientes"""

    def __init__(self, name, days, time, teacher):
        self.name = name
        self.days = days
        self.time = time
        self.teacher = teacher


class ListClubDisciplines(Resource):
    """Recurso de disciplinas del club de la API"""

    def get(self):
        """Define el metodo get (listar disciplinas del club) de la API"""

        dis_list = disciplines.list_all_enabled_disciplines()
        disciplines_json = []
        for dis in dis_list:
            categories_json = []
            for cat in dis.categories:
                categories_json.append(dict({
                    'name': cat.name,
                    'instructors': cat.instructors,
                    'days': cat.days,
                    'hour_fence': cat.hour_fence
                }))
            discipline_json = dict({
                'name': dis.name,
                'monthly_price': dis.monthly_price,
                'categories': categories_json
            })
            disciplines_json.append(discipline_json)
        return jsonify(disciplines_json)


class ListMyDisciplines(Resource):
    """Recurso de disciplinas que practica un asociado de la API"""

    @jwt_required()
    def get(self):
        """Define el metodo get (listar las disciplinas que practico) de la API"""

        id = get_jwt_identity()
        associate = associates.get_associate_by_id(id)
        try:
            dis_list = associate.disciplines_practiced
            disciplines_json = []
            for dis in dis_list:
                categories_json = []
                for cat in dis.categories:
                    categories_json.append(dict({
                        'name': cat.name,
                        'instructors': cat.instructors,
                        'days': cat.days,
                        'hour_fence': cat.hour_fence
                    }))
                discipline_json = dict({
                    'name': dis.name,
                    'monthly_price': dis.monthly_price,
                    'categories': categories_json
                })
                disciplines_json.append(discipline_json)
            return jsonify(disciplines_json)
        except:
            return abort(401)


class PaymentObj(object):
    """Clase que define el objeto pago devuelto por la API con los campos correspondientes"""

    def __init__(self, id, month, amount, paid, year, surcharge=0, expiration_date=None):
        self.id = id
        self.month = month
        self.year = year
        self.amount = amount
        self.paid = paid
        self.surcharge = surcharge
        self.expiration_date = expiration_date


class ListMyPayments(Resource):
    """Recurso de pagos de la API"""

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self):
        """Define el metodo get (listar mis pagos) de la API"""

        id = get_jwt_identity()
        associate = associates.get_associate_by_id(id)

        if associate:
            list_fees = associate.fees
            list_payments = []
            for fee in list_fees:
                if (fee.paid):
                    paym = PaymentObj(
                        id=fee.id, month=fee.month, year=fee.year, paid=True, amount=fee.receipt.amount_paid)
                    list_payments.append(paym.__dict__)
                else:
                    today = date.today()
                    if (fee.year <= today.year or fee.month <= today.month):
                        amount_to_pay = fee.amount_to_pay
                        percentage = 0
                        if (date.fromisoformat(str(fee.expiration_date)) < today):
                            percentage = adminConfig.list_config().porcentaje_recargo
                            amount_to_pay = amount_to_pay * \
                                (percentage * 0.01) + amount_to_pay
                        paym = PaymentObj(
                            id=fee.id,
                            month=fee.month,
                            year=fee.year,
                            paid=False,
                            amount=amount_to_pay,
                            surcharge=percentage,
                            expiration_date=fee.expiration_date
                        )
                        list_payments.append(paym.__dict__)
            return jsonify(list_payments)
        else:
            return abort(401)

    @jwt_required()
    def post(self):
        """Define el metodo POST (Registrar pago) de la API"""

        self.parser.add_argument(
            "paid_by", type=str, required=True, location="json")
        self.parser.add_argument(
            "payment_date", type=str, required=True, location="json")
        self.parser.add_argument(
            "fee_id", type=int, required=True, location="json")
        self.parser.add_argument(
            "amount_paid", type=int, required=True, location="json")
        self.parser.add_argument(
            "image", type=str, required=True, location="json")

        args = self.parser.parse_args()

        id = get_jwt_identity()
        data = request.json
        assoc = associates.get_associate_by_id(id)
        if assoc:
            fee = payments.get_fee_by_id(data["fee_id"])
            if (fee) and (fee in assoc.fees) and (not fee.paid):
                data["payment_date"] = datetime.strptime(
                    data["payment_date"], "%d/%m/%Y").date()
                new_receipt = {
                    'payment_date': data['payment_date'],
                    'amount_paid': data['amount_paid'],
                    'paid_by': data['paid_by'],
                    'fee': fee
                }
                
                receipt = payments.create_receipt(**new_receipt)
                # Save the file
                try:
                    file_header, file_content_b64 = data['image'].split(',')
                    extension = file_header.split(';')[0].split('/')[1]
                    file_bytes = base64.b64decode(file_content_b64)
                    file = open(Path(Path(__file__).parent.parent.parent.parent, "private","receipts","recibo_de_{id_ass}_nro_{receipt_id}.{ext}".format(
                        id_ass=assoc.id, receipt_id=receipt.id, ext=extension)), "wb")
                    file.write(file_bytes)
                    file.close()
                except:
                    abort(500)
                payments.pay_fee_and_assign_receipt(fee, receipt)
            else:
                # UNPROCESSABLE ENTITY (Sintaxis correcta, pero no se pudo procesar la instruccion)
                abort(422)
        else:
            abort(401)

        return jsonify(
            PaymentObj(
                id=fee.id,
                month=fee.month,
                year=fee.year,
                amount=new_receipt['amount_paid'],
                paid=True
            ).__dict__
        )


class Login(Resource):
    """Recurso de autenticación de socios de la API"""

    parser = reqparse.RequestParser()

    def post(self):
        """Define el metodo POST Login de la API"""

        self.parser.add_argument(
            "user", type=str, required=True, location="json")
        self.parser.add_argument(
            "password", type=str, required=True, location="json")
        data = request.json
        if "user" in data:
            dni = data['user']
        else:
            return abort(400)
        if "password" in data:
            password = data['password']
        else:
            return abort(400)
        user = associates.find_associate_by_dni_and_pass(dni, password)

        if user:
            access_token = create_access_token(identity=user.id)
            response = jsonify(access_token)
            set_access_cookies(response, access_token)
            return response
        else:
            return abort(401)


class Logout(Resource):
    """Recurso de cierre de sesión de socios de la API"""

    @jwt_required(verify_type=False)
    def delete(self):
        """Define el metodo DELETE Logout de la API"""

        response = jsonify()
        unset_jwt_cookies(response)

        return response, 200


class Profile(Resource):
    "Recurso que devuelve los datos de perfil del usuario"

    @jwt_required()
    def get(self):
        "Define el metodo GET para obtener los datos de perfil del usuario actualmente logueado"

        id = get_jwt_identity()
        user = associates.get_associate_by_id(id)

        if user:
            response = user.to_dict()
            return jsonify(response)
        else:
            abort(401)


class EstadisticasAsociadosPorGenero(Resource):
    "Devuelve las estadisticas de los asociados por genero"

    @jwt_required(locations=["headers"])
    def get(self):
        m = associates.count_all_associates_filter_by_genere_masculine()
        f = associates.count_all_associates_filter_by_genere_femenine()
        o = associates.count_all_associates_filter_by_genere_other()
        response = dict(masculino=m, femenino=f, otro=o)
        return jsonify(response)


class EstadisticasDisciplinasPorEdad(Resource):
    "Devuelve las estadisticas de asociados por edad"

    @jwt_required()
    def get(self):
        a = associates.count_all_asociates_by_age()
        return jsonify(a)


class EstadisticasAsociadosActivosNoActivos(Resource):
    "Devuelve las estadisticas de asociados activos y no activos"

    @jwt_required(locations=["headers"])
    def get(self):
        noActivos = associates.list_all_associates_filter_by_status(False)
        activos = associates.list_all_associates_filter_by_status(
            True)
        response = dict(activos=len(activos), noActivos=len(noActivos))
        return jsonify(response)


class MiCarnet(Resource):
    "Recurso que devuelve los datos del socio y el estado de su cuenta"

    @jwt_required()
    def get(self):

        id = get_jwt_identity()
        user = associates.get_associate_by_id(id)

        if user:
            list_fees = user.fees
            debt = False
            for fee in list_fees:
                if (not fee.paid):
                    today = date.today()
                    if (date.fromisoformat(str(fee.expiration_date)) < today):
                        debt = True
                        break
            response = dict()

            if (debt and not user.status):
                response["status"] = "Inhabilitado y deudor"
                response["description"] = dict_status[response["status"]]
            elif debt:
                response["status"] = "Deudor"
                response["description"] = dict_status[response["status"]]
            elif not user.status:
                response["status"] = "Inhabilitado"
                response["description"] = dict_status[response["status"]]
            else:
                response["status"] = "Inhabilitado y deudor"
                response["description"] = dict_status[response["status"]]

            response["profile"] = user.to_dict()
            return jsonify(response)
        else:
            abort(401)


class ListAllDisciplines(Resource):
    "Devuelve todas las disciplinas"
    @jwt_required()
    def get(self):
        dis = disciplines.list_all_disciplines()
        resp = []
        for i in dis:
            resp.append(i.to_dict())
        return jsonify(resp)


class StatsDiscipline(Resource):
    "Devuelve las estadisticas de las disciplinas"

    @jwt_required()
    def get(self):
        args = request.args
        dis = args['discipline']
        mascCount = 0
        femCount = 0
        otherCount = 0
        arr = [0] * 100
        aso = associates.list_all_associates()
        ahora = datetime.now()
        for i in aso:
            for e in i.disciplines_practiced:
                if (e.id == int(dis)):
                    asodict = i.to_dict()
                    age = int((ahora - i.date_of_birth).days/365)
                    arr[age] = arr[age] + 1
                    if (asodict["gender"] == "Femenino"):
                        femCount = femCount+1
                    elif (asodict["gender"] == "Masculino"):
                        mascCount = mascCount+1
                    else:
                        otherCount = otherCount + 1
        response = dict(masculino=mascCount, femenino=femCount,
                        otro=otherCount, edades=arr)
        return jsonify(response)


class ClubInfo(Resource):
    "Recurso para acceder a la información de contacto del club"

    def get(self):
        "Devuelve la información de contacto del club"

        config = adminConfig.list_config()
        dict = {"contacto": config.info_contacto}
        return jsonify(dict)
