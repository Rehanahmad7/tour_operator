import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(_file_).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret")
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS: allow Vercel domains
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".vercel.app,localhost").split(",")

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # whitenoise for static files
    # ... other middleware
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # fallback to sqlite for local dev (but don't commit sqlite to production)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
