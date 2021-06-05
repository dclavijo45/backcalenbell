import time
from flask.views import MethodView
from flask import redirect
from models.model import Models
from config.config import SERVER_FRONT


class ManageQueryFriendsControllers(MethodView):
    def get(self, token):
        Model = Models()
        Model.info = {"token": token}

        Model.manageQueryFriendsM()

        return redirect(SERVER_FRONT + "/chat", code=302)
