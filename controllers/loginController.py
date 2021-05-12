import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class LoginUserControllers(MethodView):
    """
        Login
    """
    def post(self):
        # time.sleep(1)
        json_request = request.get_json(force=True)

        Model = Models()

        id_token = fixStringClient(json_request.get("id_token")) if json_request.get("id_token") != None else None

        Model.info = {
            'user': fixStringClient(json_request.get("user")),
            'password': fixStringClient(json_request.get("password")),
            'type': fixStringClient(json_request.get("type")),
            'id_token': id_token
        }
        dataDB = Model.login()
        
        return jsonify(dataDB), 200
