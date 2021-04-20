from controllers import *

user = {
    "login_user": "/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    
    "register_user": "/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),

    "recovery_account": "/user/recovery", "recovery_account_controllers": RecoveryAccountControllers.as_view("recovery_account_api"),

    "validate_code_recovery_account": "/user/validate/recoverycode", "validate_code_recovery_account_controllers": ValidateCodeRecoveryAccountControllers.as_view("validate_code_recovery_account_api"),

    "change_pwd": "/user/validate/changepwd", "change_pwd_controllers": validateChangePwdControllers.as_view("change_pwd_api"),
}

admin = {
    "manage_events": "/user/manage/events", "manage_events_controllers": EventsControllers.as_view("manage_events_api"),
}