from .settings import *

# Use an in-memory SQLite database for faster testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        },
    }
}

# Disable migrations for testing
MIGRATION_MODULES = {app.split('.')[-1]: None for app in INSTALLED_APPS if app.startswith('django.') is False}

# Turn off password hashing for faster tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Configure static files for testing
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

# Disable debug mode for testing
DEBUG = False

# Disable signals during tests to prevent automatic creation of PlayerStats
TESTING = True
