from .base import *

DEBUG = False

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'calendar_app',
        'USER': 'postgres',
        'PASSWORD': 'c@lend@r',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 300,
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test.calendar_app.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
}

# for interacting with timekit
TIMEKIT_APP_NAME = "test-101"
TIMEKIT_API_BASE_URL = "https://api.timekit.io/v2"

# for JWT encoding/decoding
JWT_SECRET_KEY = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_AUTH_HEADER_PREFIX = 'JWT'
