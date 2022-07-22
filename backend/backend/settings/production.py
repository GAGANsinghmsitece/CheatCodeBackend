from .base import *

DEBUG=False

ALLOWED_HOSTS+=['cheatcode.pythonanywhere.com','pythonanywhere.com']

SECURE_SSL_REDIRECT = True


ROOT_URLCONF = 'backend.urls.production'