# REFACTOR: use env() and 'harden'
import environ
import os
import io
from google.cloud import secretmanager
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, 'config/.env')

print("checking for local ENV: " + env_file)

if os.path.isfile(env_file):
    # read a local .env file
    env.read_env(env_file)

elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
    # pull .env definitions from Secret Manager
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    print(f'Using Google SECRETS:{project_id}')
    
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get('SETTINGS_NAME', 'pfolio-backend-secret')
    name = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
    payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')

    env.read_env(io.StringIO(payload))
else:
    raise Exception('No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.')

# #load_dotenv()  # take environment variables from .env.

FRONTEND_URL=os.getenv('FRONTEND_URL').rstrip("/")
print(f"\nFRONTEND_URL::{FRONTEND_URL}")

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL
]
 
SECRET_KEY = os.getenv('SECRET_KEY')
# print("SECRET_KEY", SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = bool(int(os.environ.get('DEBUG',0)))
#print("DEBUG::", env('DEBUG'))

# when DEBUG = False : Not Found The requested resource was not found on this server.
# research cause of this
# test running as production in local env
#
# https://stackoverflow.com/questions/1626326/how-to-manage-local-vs-production-settings-in-django
# restructure to specific production & local settings
#
DEBUG=os.getenv('DEBUG')
print("DEBUG::", DEBUG)

APPENGINE_URL = env('APPENGINE_URL', default=None)
if APPENGINE_URL:
    # ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f'https://{APPENGINE_URL}'

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ['*']

DATABASES = {'default': env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 1234
    
#ALLOWED_HOSTS = [
#    '0.0.0.0',
#    'backend',
#    'localhost',
#    '127.0.0.1',
#    '*',
#]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'corsheaders',

    # Local
    'about',
    'projects',
    'technologies',
    'qualifications',
    'contact',
    'upload',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('postgres'),
#         #'HOST': '35.189.112.171',
#         #'HOST': '10.154.0.3',   # insternal IP
#         'PORT': os.getenv('POSTGRES_PORT'),
# #        'PORT': '', # leave blank so the default port is selected
#     }
# }


# LOCAL_DB=env('POSTGRES_DB')
# print(f'LOCAL DB:{LOCAL_DB}')
 
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': env('POSTGRES_DB'),
#        'USER': env('POSTGRES_USER'),
#        'PASSWORD': env('POSTGRES_PASSWORD'),
#        'HOST': env('POSTGRES_HOST'),
#        'PORT': '', # leave blank so the default port is selected
#        'PORT': '', # leave blank so the default port is selected
#    }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# MEDIA_ROOT is for the user-uploaded content

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static')
]

from google.oauth2 import service_account
# storage

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'config/heidless-pfolio-deploy-9-5bab8c3949ac.json')
)

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_BUCKET_NAME = 'heidless-pfolio-deploy-9-bucket'

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

#STATIC_URL = '/static/'
STATIC_URL = 'https://storage.cloud.google.com/heidless-pfolio-deploy-9-bucket/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
# MEDIA_URL = 'https://storage.cloud.google.com/pfolio-backend-bucket-4/media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FILE_UPLOAD_PERMISSIONS=0o640