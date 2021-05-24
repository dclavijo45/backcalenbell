import time
from flask.views import MethodView
from flask import jsonify, request
from services.services import fixStringClient
from models.model import Models

class SearchContactsControllers(MethodView):
    """
        Search users
    """
    def post(self):
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        json_request = request.get_json()

        Model = Models()
        Model.info = {
            'token': token,
            'search_key': fixStringClient(json_request.get('search_key'))
        }
        data = Model.searchContacts()

        # time.sleep(1)
        return jsonify(data), 200