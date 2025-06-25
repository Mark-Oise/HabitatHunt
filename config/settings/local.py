"""
Local development settings for config project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s74uw5q)=0j0-r)akx9p!-m6dn^kgtb3%j30npc%qv9ef1h9_g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files for development
STATIC_ROOT = BASE_DIR / 'static'
COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = False  # Disable compression in development

# Read environment variables for local development
environ.Env.read_env()
