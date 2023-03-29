from pathlib import Path
import os
import RPi.GPIO as gp
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(38 , gp.OUT)
gp.setup(40 , gp.OUT)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#=sgi_vuwf@(zisa4u5r8rgi!rfg#nq0i1g_8^h#@nu7ic-0$('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*","https://7f23-103-90-97-197.in.ngrok.io" , "7f23-103-90-97-197.in.ngrok.io"]

CSRF_TRUSTED_ORIGINGS = ["*" , "https://*.in.ngrok.io" ,"https://7f23-103-90-97-197.in.ngrok.io"]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'base.apps.BaseConfig',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
    
ROOT_URLCONF = 'HackBios.urls'

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

WSGI_APPLICATION = 'HackBios.wsgi.application'
ASGI_APPLICATION = "HackBios.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

CORS_ALLOW_ALL_ORIGIN = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    "default" : {
            "BACKEND" : "channels.layers.InMemoryChannelLayer"
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LOGIN_URL = "login-user"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR , "static_cdn")
MEDIA_ROOT = os.path.join(BASE_DIR , "media_cdn")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR , "static") ,
    os.path.join(BASE_DIR , "media") ,
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

