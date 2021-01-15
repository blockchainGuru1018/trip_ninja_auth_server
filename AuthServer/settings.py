import os
from decouple import config

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = os.environ.get('DEBUG', False)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'asdfasdfasdfasdfasdfasdfs'
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = "users.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_js_reverse",
    'rest_framework',
    'rest_framework.authtoken',
    "import_export",
    "rest_auth",
    'django.contrib.sites',
    'rest_auth.registration',
    'corsheaders',
    'api',
    'common',
    'teams',
    'users',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.psutil',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]


ROOT_URLCONF = 'AuthServer.urls'

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'AuthServer.wsgi.application'

LOCAL_DEV_URL = 'http://127.0.0.2:8000'

SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = (
    LOCAL_DEV_URL,
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    'http://tripninja-quicktrip-dev.s3-website-us-east-1.amazonaws.com'
)

CORS_ORIGIN_WHITELIST = (
    LOCAL_DEV_URL,
    'https://.elasticbeanstalk.com',
    'https://.amazonaws.com',
    'http://tripninja-quicktrip-dev.s3-website-us-east-1.amazonaws.com'
)

CSRF_TRUSTED_ORIGINS = [".elasticbeanstalk.com", ".tripninja.io"]
CSRF_COOKIE_DOMAIN = LOCAL_DEV_URL
CSRF_USE_SESSION = True
CSRF_COOKIE_NAME = 'csrf_token'
CSRF_COOKIE_SECURE = False

STATIC_URL = './static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    BASE_DIR]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FIXTURE_DIRS = ['fixtures']

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

    #AWS X-Ray
    MIDDLEWARE += [
        'aws_xray_sdk.ext.django.middleware.XRayMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ]

    INSTALLED_APPS += ['aws_xray_sdk.ext.django']

    XRAY_RECORDER = {
        'AWS_XRAY_DAEMON_ADDRESS': '127.0.0.1:2000',
        'AUTO_INSTRUMENT': True,
        # If turned on built-in database queries and template rendering will be recorded as subsegments
        'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR',
        'PLUGINS': (),
        'SAMPLING': True,
        'SAMPLING_RULES': None,
        'AWS_XRAY_TRACING_NAME': "AuthServer",  # the segment name for segments generated from incoming requests
        'DYNAMIC_NAMING': None,  # defines a pattern that host names should match
        'STREAMING_THRESHOLD': None,  # defines when a segment starts to stream out its children subsegments
    }

    API_URL = os.getenv('API_URL')
else:
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }
    API_URL = 'http://127.0.0.1:8000/'



if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    API_URL = os.getenv('API_URL')


REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'api.serializers.LoginSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
