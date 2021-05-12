import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class RecoveryAccountControllers(MethodView):
    def post(self):
        json_request = request.get_json(force=True)

        Model = Models()

        Model.info = {
            'account': fixStringClient(json_request.get("account")),
            'type': fixStringClient(json_request.get("type"))
        }

        dataDB = Model.recoveryAccount()
        
        return jsonify(dataDB), 200
