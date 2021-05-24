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
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json(force=True)

        Model = Models()
        Model.info = {
            'token': token,
            'user_add': fixStringClient(json_request.get("user_add"))
        }
        data = Model.addContacts()

        # time.sleep(1)
        return jsonify(data), 200

    def delete(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        payload = request.headers.get('Body').split(" ")[1] if request.headers.get('Body') else None # pos: 1 = id_contactG, 2 = type contact

        Model = Models()
        Model.info = {
            'token': token,
            'payload': fixStringClient(payload)
        }
        data = Model.deleteContacts()

        # time.sleep(1)
        return jsonify(data), 200