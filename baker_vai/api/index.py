import os
import sys

# Make the project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baker_vai.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
