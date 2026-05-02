import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

ROOT_DIR = Path(__file__).resolve().parent.parent
DJANGO_PROJECT_ROOT = ROOT_DIR / "UniCart"

if str(DJANGO_PROJECT_ROOT) not in sys.path:
    sys.path.append(str(DJANGO_PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UniCart.settings")

app = get_wsgi_application()