import os
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Agregar la carpeta services a sys.path para encontrar la app chat
sys.path.insert(0, str(BASE_DIR / "services"))


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-secret-key-for-dev-only-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'chat',
    'corsheaders',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

REST_AUTH = {
    'USE_JWT': True,
    'TOKEN_MODEL': None,
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_RETURN_EXPIRATION': False,
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
    'PASSWORD_RESET_SERIALIZER': 'nura.serializers.CustomPasswordResetSerializer',
    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

ACCOUNT_ADAPTER = 'nura.adapters.NuraAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
LOGIN_ON_EMAIL_CONFIRMATION = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if os.getenv('MAILGUN_API_KEY') and os.getenv('MAILGUN_DOMAIN'):
    EMAIL_BACKEND = 'nura.mail_backend.MailgunAPIBackend'
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', f'no-reply@{os.getenv("MAILGUN_DOMAIN")}')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
ROOT_URLCONF = 'nura.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'nura' / 'templates'],
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


WSGI_APPLICATION = 'nura.wsgi.application'


# Database
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is required - set it in your .env file")
parsed = urlparse(DATABASE_URL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed.path.lstrip('/'),
        'USER': unquote(parsed.username or ''),
        'PASSWORD': unquote(parsed.password or ''),
        'HOST': parsed.hostname or '',
        'PORT': parsed.port or '5432',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

# Media files (uploads) - Supabase Storage
# Supabase Storage is S3-compatible
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Supabase S3 Configuration
S3_ACCESS_KEY_ID = os.getenv('SUPABASE_ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY = os.getenv('SUPABASE_SECRET_ACCESS_KEY')
S3_STORAGE_BUCKET_NAME = os.getenv('SUPABASE_BUCKET_NAME', 'nura-datasets')
S3_ENDPOINT_URL = f"https://{os.getenv('SUPABASE_PROJECT_ID')}.supabase.co/storage/v1/s3"
S3_REGION_NAME = 'us-east-1'  # Default for Supabase
S3_FILE_OVERWRITE = False
S3_DEFAULT_ACL = 'public-read'  # Or 'private' depending on your needs
S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Optional: If you want to use custom domain
# AWS_S3_CUSTOM_DOMAIN = f"{os.getenv('SUPABASE_PROJECT_ID')}.supabase.co/storage/v1/object/public/{S3_STORAGE_BUCKET_NAME}"

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage' if not DEBUG else 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
