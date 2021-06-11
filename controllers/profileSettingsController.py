import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient, fixBase64String
from models.model import Models

class ProfileSettingsControllers(MethodView):
    def post(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json(force=True)

        Model = Models()
        Model.info = {
            'token': token,
            'action': fixStringClient(json_request.get("action")),
            'area': fixStringClient(json_request.get("area")),
            'resource' : fixBase64String(json_request.get("resource")),
        }
        data = Model.settingsUser()

        # time.sleep(1)
        return jsonify(data), 200