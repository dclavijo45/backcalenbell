from flask import Flask
from flask_cors import CORS
from routes.routes import *
from config.config import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY

CORS(
    app,
    resources={
        r"/*": {"origins": "*"},
        r"/*": {
            "origins": ["*"],
            "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Authorization", "Content-Type", "Body"],
        },
    },
)

app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])

app.add_url_rule(user["register_user"], view_func=user["register_user_controllers"])

app.add_url_rule(logged["manage_events"], view_func=logged["manage_events_controllers"])

app.add_url_rule(
    user["recovery_account"], view_func=user["recovery_account_controllers"]
)

app.add_url_rule(
    user["validate_code_recovery_account"],
    view_func=user["validate_code_recovery_account_controllers"],
)

app.add_url_rule(user["change_pwd"], view_func=user["change_pwd_controllers"])

app.add_url_rule(logged["init_chat"], view_func=logged["init_chat_controllers"])

app.add_url_rule(
    logged["manage_contactsG"], view_func=logged["manage_contactsG_controllers"]
)

app.add_url_rule(
    logged["search_contacts"], view_func=logged["search_contacts_controllers"]
)

app.add_url_rule(
    logged["manage_query_friends"], view_func=logged["manage_query_friends_controllers"]
)

app.add_url_rule(
    logged["participants_event"], view_func=logged["participants_event_controllers"]
)

app.add_url_rule(logged["join_event"], view_func=logged["join_event_controllers"])

app.add_url_rule(
    logged["delete_participant_event"],
    view_func=logged["delete_participant_event_controllers"],
)
