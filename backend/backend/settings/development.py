from .base import *

DEBUG = True

INSTALLED_APPS+=[
    'silk'
]
MIDDLEWARE+=[
    'silk.middleware.SilkyMiddleware'
]

ROOT_URLCONF = 'backend.urls.development'