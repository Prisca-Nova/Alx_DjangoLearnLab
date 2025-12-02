# LibraryProject/settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
# Always set DEBUG to False in production environment
DEBUG = False  # Changed from True for production security

ALLOWED_HOSTS = ['*']  # In production, specify actual domain names

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'csp',  # Added for Content Security Policy
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',  # Added for CSP support
    'django.middleware.security.SecurityMiddleware',  # For security headers
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.backends.BigAutoField'

# ==================== SECURITY SETTINGS ====================

# Security middleware settings
SECURE_BROWSER_XSS_FILTER = True  # Enables browser's XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents MIME type sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevents clickjacking by denying framing

# Cookie security - Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS
SESSION_COOKIE_SECURE = True  # Session cookies only over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie

# HTTPS settings (uncomment in production with HTTPS)
# SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
# SECURE_HSTS_SECONDS = 31536000  # Enable HSTS for 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Content Security Policy (CSP) Settings
# Prevents XSS attacks by specifying allowed content sources
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Allow inline styles for compatibility
CSP_SCRIPT_SRC = ("'self'",)  # Only allow scripts from same origin
CSP_IMG_SRC = ("'self'", "data:")  # Allow images from same origin and data URIs
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)  # Disallow plugins like Flash
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Prevents framing