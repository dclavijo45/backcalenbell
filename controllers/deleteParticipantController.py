import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models


class DeleteParticipantControllers(MethodView):
    def post(self):
        token = (
            request.headers.get("Authorization").split(" ")[1]
            if request.headers.get("Authorization")
            else None
        )

        json_request = request.get_json(force=True)

        Model = Models()
        Model.info = {
            "token": token,
            "id_event": fixStringClient(json_request.get("id_event")),
            "user_delete": fixStringClient(json_request.get("user_delete")),
        }
        data = Model.deleteParticipants()

        # time.sleep(1)
        return jsonify(data), 200
