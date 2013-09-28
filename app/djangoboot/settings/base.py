import os

from django.conf import global_settings


APP_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def rel(*x):
    return os.path.join(APP_ROOT, *x)


#defined in secrets.py
DATABASE_USER = None
DATABASE_PASSWORD = None
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
SOCIAL_AUTH_GITHUB_KEY = None
SOCIAL_AUTH_GITHUB_SECRET = None


try:
    from secrets import *
except ImportError:
    pass


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sebastian Nogara', 'snogaraleal@gmail.com'),
    ('Pablo Ricco', 'pricco@gmail.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangoboot',
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': ''
    }
}

ALLOWED_HOSTS = []


TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True


AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = False


MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'
MEDIA_BUCKET = None
MEDIA_LOCATION = None
MEDIA_DOMAIN = None
MEDIA_HEADERS = {
    'Expires': 'Thu, 31 Dec 2050 00:00:00 GMT',
    'Cache-Control': 'max-age=315360000, public',
}
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


STATIC_ROOT = rel('assets')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel('static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_BUCKET = None
STATIC_LOCATION = None
STATIC_DOMAIN = None
STATIC_HEADERS = {
    'Expires': 'Thu, 31 Dec 2050 00:00:00 GMT',
    'Cache-Control': 'max-age=315360000, public',
}
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SECRET_KEY = 'a1gf&i7+&+p7lkuazmvvw4g(w5ce(=i=k!quypy%q8-!tx=3*8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
TEMPLATE_DIRS = (
    rel('templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'djangoboot.urls'

WSGI_APPLICATION = 'djangoboot.wsgi.application'

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS = (
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.github.GithubOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'accounts.pipeline.store_redirect',
)


SOCIAL_AUTH_USER_MODEL = 'accounts.User'

SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'south',
    'taggit',
    'storages',

    'core',
    'accounts',
    'boots',
    'home',

    'social.apps.django_app.default',
)

RESERVED_SLUGS = ['create', 'update', 'delete']

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_USER_MODEL = 'accounts.User'