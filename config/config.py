from os import environ as env

#   app config
KEY_TOKEN_AUTH = env['key_auth_token']
SECRET_KEY = env['secret_key']
HIGH_SECRET_KEY_PWD = env['high_secret_key_pwd']
SERVER_FRONT = env['SERVER_FRONT']
SERVER_BACK = env['SERVER_BACK']

# MySQL config 
MYSQL_DB = env['mysql_db']
MYSQL_PASSWORD = env['mysql_password']
MYSQL_PORT = env['mysql_port']
MYSQL_USER = env['mysql_user']
MYSQL_HOST = env['mysql_host']

#   mailconfig
PROVEEDOR_MAIL = env['proveedor_mail']
CORREO_MAIL = env['correo_mail']
PASSWORD_MAIL = env['password_mail']

# # DropBox Config
ACCESS_TOKEN = ''


# Google Auth API
AUDIENCE_AUTH2 = env['key_audience_google']


# SMS API
API_AUTH2_SMS_env = env['api_sms']
API_QUERY_CREDITS_SMS_env = env['api_query_credits_sms']
