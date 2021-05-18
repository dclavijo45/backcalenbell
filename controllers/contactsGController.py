import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class ContactsGControllers(MethodView):
    def get(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        Model = Models()
        Model.info = {
            'token': token
        }
        data = Model.getContactsG()

        # time.sleep(1)
        return jsonify(data), 200
    
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass