import time
from flask.views import MethodView
from flask import redirect
from models.model import Models
from config.config import SERVER_FRONT


class JoinEventControllers(MethodView):
    def get(self, token):
        Model = Models()

        Model.info = {"token": token}

        Model.joinParticipantsEvents()

        return redirect(SERVER_FRONT + "/home", code=302)
