from settings import *

DEBUG = TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'booklog',
         'USER': 'booklog',
         'PASSWORD':'password',
         'HOST' : '',
         'PORT' : '',
     }
}