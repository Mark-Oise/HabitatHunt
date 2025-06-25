"""
Production settings for config project.
"""

from .base import *

# Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = [
    '13.48.190.5',
    'habitathunt.com',
    'www.habitathunt.com',
    'habitathunt.onrender.com',
]

# Database for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Static files for production
STATIC_ROOT = BASE_DIR / 'static'
COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = True

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
