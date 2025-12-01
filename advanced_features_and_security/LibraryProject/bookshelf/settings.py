# Add this line
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Make sure bookshelf is in INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',  # This line must be present
]