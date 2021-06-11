from controllers.eventsController import EventsControllers
from controllers.loginController import LoginUserControllers
from controllers.registerController import RegisterUserControllers
from controllers.recoveryAccountController import RecoveryAccountControllers
from controllers.validateChangePwdController import validateChangePwdControllers
from controllers.validateCodeRecoveryController import (
    ValidateCodeRecoveryAccountControllers,
)
from controllers.initChatController import InitChatControllers
from controllers.contactsGController import ContactsGControllers
from controllers.searchContactsController import SearchContactsControllers
from controllers.manageQueryFriendsController import ManageQueryFriendsControllers
from controllers.participantsEventController import ParticipantsEventControllers
from controllers.joinEventController import JoinEventControllers
from controllers.deleteParticipantController import DeleteParticipantControllers
from controllers.profileSettingsController import ProfileSettingsControllers

user = {
    "login_user": "/user/login",
    "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "register_user": "/user/register",
    "register_user_controllers": RegisterUserControllers.as_view("register_api"),
    "recovery_account": "/user/recovery",
    "recovery_account_controllers": RecoveryAccountControllers.as_view(
        "recovery_account_api"
    ),
    "validate_code_recovery_account": "/user/validate/recoverycode",
    "validate_code_recovery_account_controllers": ValidateCodeRecoveryAccountControllers.as_view(
        "validate_code_recovery_account_api"
    ),
    "change_pwd": "/user/validate/changepwd",
    "change_pwd_controllers": validateChangePwdControllers.as_view("change_pwd_api"),
}

logged = {
    "manage_events": "/user/manage/events",
    "manage_events_controllers": EventsControllers.as_view("manage_events_api"),
    "init_chat": "/user/init/chat",
    "init_chat_controllers": InitChatControllers.as_view("init_chat_api"),
    "manage_contactsG": "/user/manage/contactsg",
    "manage_contactsG_controllers": ContactsGControllers.as_view(
        "manage_contactsG_api"
    ),
    "search_contacts": "/user/search/contacts",
    "search_contacts_controllers": SearchContactsControllers.as_view(
        "search_contacts_api"
    ),
    "manage_query_friends": "/user/manage/query/friends/<string:token>/",
    "manage_query_friends_controllers": ManageQueryFriendsControllers.as_view(
        "manage_query_friends_api"
    ),
    "participants_event": "/user/participantsevent/<string:id_event>/",
    "participants_event_controllers": ParticipantsEventControllers.as_view(
        "participants_event_api"
    ),
    "join_event": "/user/join/event/<string:token>/",
    "join_event_controllers": JoinEventControllers.as_view("join_event_api"),

    "delete_participant_event": "/user/delete/participant/",
    "delete_participant_event_controllers": DeleteParticipantControllers.as_view(
        "delete_participant_event_api"
    ),

    "profile_settings": "/user/profile/settings/",
    "profile_settings_controllers": ProfileSettingsControllers.as_view(
        "profile_settings_api"
    ),    
}
