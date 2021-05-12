import varenviron
from __init__ import app
from os import environ as env

PORT = env['PORT'] if env['PORT'] else 3000

DEBUG = True if env['DEBUG'] == '1' else False

HOST = env['HOST'] if env['HOST'] else 'localhost'

app.run(port=PORT, debug=DEBUG)
