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

STATICFILES_DIRS = (
    '/home/ubuntu/booklog/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)