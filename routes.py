from controllers import LoginUserControllers, RegisterUserControllers

user = {
    "login_user": "/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    
    "register_user": "/user/register", "register_user_controllers": RegisterUserControllers.as_view("register_api"),
}