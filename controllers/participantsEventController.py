import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models


class ParticipantsEventControllers(MethodView):
    def get(self, id_event):
        token = (
            request.headers.get("Authorization").split(" ")[1]
            if request.headers.get("Authorization")
            else None
        )

        Model = Models()
        Model.info = {"token": token, "id_event": fixStringClient(id_event)}
        data = Model.getParticipantsEvents()

        # time.sleep(1)
        return jsonify(data), 200

    def post(self, id_event):
        token = (
            request.headers.get("Authorization").split(" ")[1]
            if request.headers.get("Authorization")
            else None
        )

        json_request = request.get_json(force=True)

        Model = Models()
        Model.info = {
            "token": token,
            "id_event": fixStringClient(id_event),
            "user_invited": fixStringClient(json_request.get("user_invited")),
        }
        data = Model.addParticipantsEvents()

        # time.sleep(1)
        return jsonify(data), 200

    # left to event
    def delete(self, id_event):
        token = (
            request.headers.get("Authorization").split(" ")[1]
            if request.headers.get("Authorization")
            else None
        )

        Model = Models()
        Model.info = {"token": token, "id_event": fixStringClient(id_event)}
        data = Model.exitParticipantEvents()

        # time.sleep(1)
        return jsonify(data), 200
