import time
from flask.views import MethodView
from flask import jsonify, request
from services import fixStringClient, decryptStringBcrypt
from services import encoded_jwt
from model import Models

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
        
class RegisterUserControllers(MethodView):
    """
        Register
    """
    def post(self):
            # time.sleep(1)
            json_request = request.get_json()
            # return jsonify({"registered": True}), 200
            
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

class EventsControllers(MethodView):
    def get(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        Model = Models()
        Model.info = {
            'token': token
        }
        data = Model.getEvents()

        time.sleep(1)
        return jsonify(data), 200

    def post(self):
        token = request.headers.get('Authorization').split(" ")[1]

        json_request = request.get_json()

        Model = Models()
        Model.info = {
            'token': token,
            'title': fixStringClient(json_request.get("title")),
            'hour': fixStringClient(json_request.get("hour")),
            'date': fixStringClient(json_request.get("date")),
            'description': fixStringClient(json_request.get("description")),
            'type_ev': fixStringClient(json_request.get("type_ev")),
            'icon': fixStringClient(json_request.get("icon")),
        }
        data = Model.registerEvents()

        time.sleep(5)
        return jsonify(data), 200

    def put(self):
        pass

    def delete(self):
        pass

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

class validateChangePwdControllers(MethodView):
    def post(self):
        json_request = request.get_json(force=True)

        Model = Models()

        Model.info = {
            'token': json_request.get("token"),
            'pwd': fixStringClient(json_request.get("pwd"))
        }

        dataDB = Model.validateChangePwd()
        
        return jsonify(dataDB), 200

