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
        content = request.get_json(force=True)
        user = fixStringClient(content.get("user"))
        password = fixStringClient(content.get("password"))

        Model = Models()
        Model.info = {
            'user': user
        }
        dataDB = Model.login()
        
        if dataDB:
            for data in dataDB:
                if decryptStringBcrypt(password, data[3]):
                    jwt = encoded_jwt(data[4])
                    return jsonify({"logged": True, "token": jwt, "name": data[0], "email": data[1], "user": data[2], "password": data[3], "private_key": int(data[4])}), 200
                else:
                    return jsonify({"logged": False}), 200
        else:
            return jsonify({"logged": False}), 200
        
class RegisterUserControllers(MethodView):
    """
        Register
    """
    def post(self):
            # time.sleep(1)
            content = request.get_json()
            name = fixStringClient(content.get("name"))
            email = fixStringClient(content.get("email"))
            user = fixStringClient(content.get("user"))
            password = fixStringClient(content.get("password"))
            # return jsonify({"registered": True}), 200
            
            Model = Models()
            Model.info = {
                'name': name,
                'email': email,
                'user': user,
                'password': password
            }
            
            data = Model.register()
            
            return jsonify({"registered": data}), 200

