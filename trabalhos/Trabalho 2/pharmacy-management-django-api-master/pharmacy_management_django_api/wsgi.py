import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_management_django_api.settings')

application = get_wsgi_application()
