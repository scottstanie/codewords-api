"""
WOLFHOUND SETTINGS
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

Please read this link to make sure your settings are ready for production:
https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
"""

import os, sys, mimetypes
import string
import random
import dj_database_url
from base.sites import SITES  # , generate_cors_whitelist

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
# to make sure if you are ready for production!

######################## IMPORTANT SETTINGS ########################

SECRET_KEY = os.environ.get('SECRET_KEY', "".join(random.choice(string.printable) for i in range(40)))
ADMIN_SITE_HEADER = SITES['default']['SITE_NAME']
SITE_ID = SITES['default']['SITE_ID']

# SECURITY WARNING: DON'T run with DEBUG = True turned on in production
DEBUG = False
ALLOWED_HOSTS = ['*']
DB_ENV = 'dev'  # 'dev' for local sqlite database, 'prod' for production database.
# DB_ENV = 'prod'  # 'dev' for local sqlite database, 'prod' for production database.

# CUSTOM USER MODEL
# See /api/models.py
AUTH_USER_MODEL = 'api.User'
# AUTH BACKENDS for django-allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Custom Social Account adapter to fix certain use cases.
SOCIALACCOUNT_ADAPTER = 'api.views.SocialAccountAdapter'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'friends',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'
    }
}


# CROSS ORIGIN RESOURCE SHARING WHITELIST
# Please check /base/sites.py before production!
# CORS_ORIGIN_WHITELIST = generate_cors_whitelist(SITES)
CORS_ORIGIN_WHITELIST = ('*',)
CORS_ALLOW_CREDENTIALS = True


#################### END OF IMPORTANT SETTINGS #####################


# APPLICATION DEFINITONS

INSTALLED_APPS = [
    # CORE REQUIRED APPS, please do not remove these:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3RD PARTY APPS, Insert 3rd party apps below here:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    # CUSTOM APPS, insert custom apps you create here:
    'api',
    'base',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.DisableCSRF',
]

ROOT_URLCONF = 'base.urls'

# REST API Settings, Permissions, and Pagination

if DEBUG is False:
    REST_RENDERER = ('rest_framework.renderers.JSONRenderer',)
else:
    REST_RENDERER = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'base.middleware.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES':
        REST_RENDERER,
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.DefaultPagination'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dist', 'templates')],
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

WSGI_APPLICATION = 'base.wsgi.application'

# DATABASE settings, obtained from server/base/sites.py
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if DB_ENV == 'prod':
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'codenames',
        'USER': '',
        'PASSWORD': '',  # DB Password
        'HOST': 'localhost',
        'PORT': 5432
    }}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

mimetypes.add_type('image/svg+xml', '.svg')  # Makes Django recognize SVG
STATIC_URL = '/dist/'
MEDIA_URL = '/media/'

# The following makes sure the same static folders are used
# in both the DEBUG environment and production:

if DEBUG is False:
    STATIC_ROOT = os.path.join(BASE_DIR, 'dist')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'dist'),
    )
