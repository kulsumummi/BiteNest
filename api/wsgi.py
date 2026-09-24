import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_buddy.settings')

# WSGI application callable for Vercel serverless function
app = get_wsgi_application()
