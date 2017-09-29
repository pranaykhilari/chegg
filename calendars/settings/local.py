from .base import *

SECRET_KEY = '0hz#d9c$*s3%h#!f(=!_4hmbfvmde&5kv10m7bqsv7n@zu8-be'

DEBUG = True

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'calendar_app1',
        'USER': 'postgres',
        'PASSWORD': 'tudip123',
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
TIMEKIT_APP_NAME = "calendar-app"
TIMEKIT_API_BASE_URL = "https://api.timekit.io/v2"

# for JWT encoding/decoding
JWT_SECRET_KEY = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_AUTH_HEADER_PREFIX = 'JWT'
