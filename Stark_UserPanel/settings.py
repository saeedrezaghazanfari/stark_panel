
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['https://panel.st4w.net', 'https://www.panel.st4w.net', 'panel.st4w.net']
# SECURE_SSL_REDIRECT = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # packs
    'captcha',
	'widget_tweaks',
    
    # Apps
    'Extentions',
    'Stark_account.apps.StarkAccountConfig',
    'Stark_panel.apps.StarkPanelConfig',
    'Stark_siteSetting.apps.StarkSitesettingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Stark_UserPanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path('templates')],
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

WSGI_APPLICATION = 'Stark_UserPanel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
###################### PostGre
# DATABASES = {
#     'default': {
#         'ENGINE': config('ENGINE_DB')
#         'NAME': config('NAME_DB')
#         'USER': config('USER_DB')
#         'PASSWORD': config('PASSWORD_DB')
#         'HOST': config('HOST_DB')
#         'PORT': config('PORT_DB')
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGES = [
	('fa', 'persian'),
	('en', 'english'),
	('ar', 'arabic'),
]
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/site_static/'
STATIC_ROOT = Path("static_cdn", "static_root")

STATICFILES_DIRS = [
	Path("assets")
]
MEDIA_URL = '/media/'
MEDIA_ROOT = Path("static_cdn", "media_root")

######### # Extra PackageS # #########

# custom user
AUTH_USER_MODEL = 'Stark_account.User'

# for captcha Error
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# custom capcha
CAPTCHA_FONT_SIZE = 80
CAPTCHA_BACKGROUND_COLOR = '#000'
CAPTCHA_FOREGROUND_COLOR = '#eeb00e'
CAPTCHA_LENGTH = 3
CAPTCHA_IMAGE_SIZE = (200, 100) 

# Email config
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST=config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT=config('EMAIL_PORT')
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')

# session time change
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 # it's seconds    // Default is 1209600 seconds thats mean: 2 weak