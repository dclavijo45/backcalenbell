import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models


class RegisterUserControllers(MethodView):
    """
        Register
    """
    def post(self):
            json_request = request.get_json()
            
            Model = Models()

            id_token = fixStringClient(json_request.get("id_token")) if json_request.get("id_token") != None else None

            Model.info = {
                'name': fixStringClient(json_request.get("name")),
                'email': fixStringClient(json_request.get("email")),
                'user': fixStringClient(json_request.get("user")),
                'password': fixStringClient(json_request.get("password")),
                'type': fixStringClient(json_request.get("type")),
                'id_token': id_token
            }
            
            data = Model.register()
            
            return jsonify(data), 200
