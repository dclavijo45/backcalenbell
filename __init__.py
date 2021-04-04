from flask import Flask
from flask_cors import CORS
from routes import *
from config import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY

CORS(app, resources={
    r"/*": {"origins": "*"},
    r"/*": {
        "origins": ["*"],
        "methods": ["OPTIONS", "POST"],
        "allow_headers": ["Authorization", "Content-Type"],
        }
    })

app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])

app.add_url_rule(user["register_user"], view_func=user["register_user_controllers"])