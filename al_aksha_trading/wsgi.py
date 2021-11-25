
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'al_aksha_trading.settings')

application = get_wsgi_application()
