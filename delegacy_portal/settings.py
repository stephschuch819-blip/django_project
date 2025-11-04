"""
Django settings for delegacy_portal project.
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Security: Restrict allowed hosts in production
if DEBUG:
    ALLOWED_HOSTS = ["*"]  # Allow all in development
else:
    ALLOWED_HOSTS = [
        'django-project-68um.onrender.com',
        'localhost',
        '127.0.0.1',
    ]

# CSRF trusted origins for browser preview
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://django-project-68um.onrender.com',
]

# Add common browser preview proxy ports in development
if DEBUG:
    for port in [28013, 50774, 51234, 52345, 53456, 51982]:
        CSRF_TRUSTED_ORIGINS.append(f'http://127.0.0.1:{port}')
        CSRF_TRUSTED_ORIGINS.append(f'http://localhost:{port}')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    'portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'portal.middleware.SecurityHeadersMiddleware',  # Custom security headers
]

ROOT_URLCONF = 'delegacy_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portal.context_processors.unread_messages_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'delegacy_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# External Database Configuration 
# Use environment variable for database URL to avoid hardcoding credentials
database_url = config(
    'DATABASE_URL',
    default='postgresql://dglegacy_user:IngQk8WI00ObsHcjrFtWDm9W6SIGW5fQ@dpg-d41o908gjchc73ds79h0-a.oregon-postgres.render.com/dglegacy'
)

DATABASES = {
    'default': dj_database_url.parse(database_url)
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# WhiteNoise configuration for serving static files
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS (HTTP Strict Transport Security) - Force HTTPS
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True

# Security Headers
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com", "cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)

# Session Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_NAME = 'dglegacy_sessionid'  # Custom name to avoid fingerprinting
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Clear session when browser closes

# CSRF Settings
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access for AJAX
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'dglegacy_csrftoken'  # Custom name
CSRF_USE_SESSIONS = False  # Use cookie-based CSRF
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Login URLs
LOGIN_URL = 'beneficiary_login'
LOGIN_REDIRECT_URL = 'beneficiary_dashboard'
LOGOUT_REDIRECT_URL = 'beneficiary_login'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'application_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'application.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'portal.security': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'portal': {
            'handlers': ['application_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
