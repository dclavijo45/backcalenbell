import time
from flask.views import MethodView
from flask import jsonify, request, redirect
from services.services import fixStringClient, decWithPass
from models.model import Models
from config.config import SERVER_FRONT

class ManageQueryFriendsControllers(MethodView):
    def get(self, token):
        Model = Models()
        Model.info = {
            'token': token
        }

        data = Model.manageQueryFriendsM()

        return redirect(SERVER_FRONT+'/chat', code=302)