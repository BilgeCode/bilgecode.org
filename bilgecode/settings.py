"""
Django settings for bilgecode project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Support for SSL with Nginx proxy
USE_SSL = os.environ.get("USE_SSL", False)
if USE_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%+q*ok06slz&5h_ssf0i8r0x9*)loi^jbp5n)b1f0vwsox4o)f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "templates")]

ALLOWED_HOSTS = ['prev.bilgecode.org', 'www.bilgecode.com', 'localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.gis',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',

    'bilgecode.apps.passage_planner',

    'bootstrapform',
    'django_tides',
    # 'djstripe',
    'rest_framework',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'bilgecode.urls'

WSGI_APPLICATION = 'bilgecode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.environ.get(
        'DB_URL',
        "postgis://localhost/bc"))
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "bilgecode", "static"),
)
MEDIA_ROOT = os.environ.get(
    'MEDIA_ROOT',
    os.path.join(BASE_DIR, "..", "media"))
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT',
    os.path.join(BASE_DIR, "..", "static"))

# all auth
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    # "django.contrib.messages.context_processors.messages",

    # Required by allauth template tags
    "django.core.context_processors.request",

    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    # dj-stripe
    # 'djstripe.context_processors.djstripe_settings',
)

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[bilgecode.com] "
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL = "/"

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', ],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',  # 'js_sdk',
        # 'LOCALE_FUNC': 'path.to.callable',
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': False}
}

SITE_ID = 1

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# STRIPE Payments
# https://github.com/eldarion/django-stripe-payments
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_9Er4D8VkLhMcbzLroR91wT3X")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_GqvdKcnH6uc2GeiVpV1DD2U0")

DJSTRIPE_PLANS = {
    "backer-1": {
        "stripe_plan_id": "one-dollar-backer",
        "name": "Boatswain",
        "description": "Monthly donation to BilgeCode.org",
        "price": 1,
        "currency": "usd",
        "interval": "month"
    },
    "backer-3": {
        "stripe_plan_id": "three-dollar-backer",
        "name": "First Mate",
        "description": "Monthly donation to BilgeCode.org",
        "price": 3,
        "currency": "usd",
        "interval": "month"
    },
    "backer-5": {
        "stripe_plan_id": "five-dollar-backer",
        "name": "Captain",
        "description": "Monthly donation to BilgeCode.org",
        "price": 5,
        "currency": "usd",
        "interval": "month"
    },
    # "backer-10": {
    #     "stripe_plan_id": "ten-dollar-backer",
    #     "name": "Admiral",
    #     "description": "Monthly donation to BilgeCode.org",
    #     "price": 10,
    #     "currency": "usd",
    #     "interval": "month"
    # },
}
