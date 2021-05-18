import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class InitChatControllers(MethodView):
    """
    init chat
    """
    def post(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json(force=True)

        Model = Models()

        Model.info = {
            'chat_type': fixStringClient(json_request.get("chat_type")),
            'receiver': fixStringClient(json_request.get("receiver")),
            'group': fixStringClient(json_request.get("group")),
            'token': token
        }
        dataDB = Model.initChatM()
        
        return jsonify(dataDB), 200
