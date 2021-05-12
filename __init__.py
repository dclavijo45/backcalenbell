from flask import Flask
from flask_cors import CORS
from routes.routes import *
from config.config import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY

CORS(app, resources={
    r"/*": {'origins': '*'},
    r"/*": {
        'origins': ['*'],
        'methods': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE'],
        'allow_headers': ['Authorization', 'Content-Type', 'Body'],
        }
    })

app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])

app.add_url_rule(user["register_user"], view_func=user["register_user_controllers"])

app.add_url_rule(admin["manage_events"], view_func=admin["manage_events_controllers"])

app.add_url_rule(user["recovery_account"], view_func=user["recovery_account_controllers"])

app.add_url_rule(user["validate_code_recovery_account"], view_func=user["validate_code_recovery_account_controllers"])

app.add_url_rule(user["change_pwd"], view_func=user["change_pwd_controllers"])

