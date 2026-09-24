import os
import sys

# Add project root directory to sys.path for Vercel imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_buddy.settings')

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

app = get_wsgi_application()

# Run database migrations and seed automatically on Vercel initialization if using SQLite
if os.getenv('VERCEL') or os.getenv('VERCEL_ENV'):
    try:
        call_command('migrate', interactive=False)
        from seed import run_seed
        run_seed()
    except Exception as e:
        print(f"Vercel DB initialization warning: {e}")
