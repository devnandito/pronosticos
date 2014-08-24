import os
import sys
sys.path = ['/var/www/html/pronostico'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'pronostico.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

