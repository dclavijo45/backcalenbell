import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class ValidateCodeRecoveryAccountControllers(MethodView):
    def post(self):
        json_request = request.get_json(force=True)

        Model = Models()

        Model.info = {
            'token': json_request.get("token"),
            'code': fixStringClient(json_request.get("code"))
        }

        dataDB = Model.validateCodeRecoveryAccount()

        return jsonify(dataDB), 200
