import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class EventsControllers(MethodView):
    def get(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        Model = Models()
        Model.info = {
            'token': token
        }
        data = Model.getEvents()

        # time.sleep(1)
        return jsonify(data), 200

    def post(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json()
        

        Model = Models()
        Model.info = {
            'token': token,
            'title': fixStringClient(json_request.get("title")),
            'hour': fixStringClient(json_request.get("hour")),
            'date': fixStringClient(json_request.get("date")),
            'description': fixStringClient(json_request.get("description")),
            'type_ev': fixStringClient(json_request.get("type_ev")),
            'icon': fixStringClient(json_request.get("icon"))
        }
        data = Model.registerEvents()

        # time.sleep(5)
        return jsonify(data), 200

    def put(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json()
        

        Model = Models()
        Model.info = {
            'token': token,
            'title': fixStringClient(json_request.get("title")),
            'hour': fixStringClient(json_request.get("hour")),
            'date': fixStringClient(json_request.get("date")),
            'description': fixStringClient(json_request.get("description")),
            'type_ev': fixStringClient(json_request.get("type_ev")),
            'icon': fixStringClient(json_request.get("icon")),
            'id_event': fixStringClient(json_request.get("id_event"))
        }
        
        data = Model.changeEvents()

        # time.sleep(5)
        return jsonify(data), 200

    def delete(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        events = request.headers.get('Body').split(" ")[1] if request.headers.get('Body') else None
        
        Model = Models()
        Model.info = {
            'token': fixStringClient(token),
            'events': fixStringClient(events)
        }

        data = Model.deleteEvents()

        # time.sleep(5)
        return jsonify(data), 200
