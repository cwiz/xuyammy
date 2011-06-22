import os

DATABASE = {
    'DATABASE_ENGINE': 'django.db.backends.sqlite3',
    'DATABASE_NAME': 'xuyammy'
}

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
LOGIN_URL = '/login'
PORT = 8888

