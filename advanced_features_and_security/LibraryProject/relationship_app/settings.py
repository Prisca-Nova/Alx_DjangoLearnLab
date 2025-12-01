# Add or modify these settings

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# Add 'users' to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Add this line
    # ... other apps
]

# Media settings for file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Update authentication backends if needed
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]