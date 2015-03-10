# -*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG
JS_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

import os
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep

CORE_PATH = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'ota.db'),       # нужно чтобы в чероки не приходилось указывать полный путь до файла с базой данных
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "ru-ru"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_PATH + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap'

MULTIUPLOADER_FILES_FOLDER = PROJECT_PATH + 'multiuploader/'
MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600
MULTIUPLOADER_FORMS_SETTINGS = {
'default': {
    'FILE_TYPES': ["txt", "zip", "jpg", "jpeg", "flv", "png", "upd", "img"],
    'CONTENT_TYPES': [
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'text/plain',
            'text/rtf',
            'application/octet-stream',
            'text/upd',
            'text/img',
            ],
    'MAX_FILE_SIZE': 10485760000,
    'MAX_FILE_NUMBER':5,
    'AUTO_UPLOAD': True,
},
'images': {
    'FILE_TYPES': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico'],
    'CONTENT_TYPES': [
        'image/gif',
        'image/jpeg',
        'image/pjpeg',
        'image/png',
        'image/svg+xml',
        'image/tiff',
        'image/vnd.microsoft.icon',
        'image/vnd.wap.wbmp',
        ],
    'MAX_FILE_SIZE': 1048576000,
    'MAX_FILE_NUMBER': 5,
    'AUTO_UPLOAD': True,
},
'video': {
    'FILE_TYPES': ['flv', 'mpg', 'mpeg', 'mp4' ,'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm'],
    'CONTENT_TYPES': [
        'video/mpeg',
        'video/mp4',
        'video/ogg',
        'video/quicktime',
        'video/webm',
        'video/x-ms-wmv',
        'video/x-flv',
        ],
    'MAX_FILE_SIZE': 1048576000,
    'MAX_FILE_NUMBER': 5,
    'AUTO_UPLOAD': True,
},
'audio': {
    'FILE_TYPES': ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm'],
    'CONTENT_TYPES': [
        'audio/basic',
        'audio/L24',
        'audio/mp4',
        'audio/mpeg',
        'audio/ogg',
        'audio/vorbis',
        'audio/x-ms-wma',
        'audio/x-ms-wax',
        'audio/vnd.rn-realaudio',
        'audio/vnd.wave',
        'audio/webm'
        ],
    'MAX_FILE_SIZE': 1048576000,
    'MAX_FILE_NUMBER': 5,
    'AUTO_UPLOAD': True,
},
'application': {
    'FILE_TYPES': ["upd", "img"],
    'CONTENT_TYPES': [
        'application/upd',
        'application/img',
        'application/octet-stream',
        ],
    'MAX_FILE_SIZE': 1048576000,
    'MAX_FILE_NUMBER': 5,
    'AUTO_UPLOAD': True,
}}
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_PATH + "ota/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.MULTIUPLOADER_FILES_FOLDER
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lvqay&_9%m^+cnw44)ah0h_2_dhrri#t2sjc2srm-qwth=*4ez'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware"
)

ROOT_URLCONF = 'ota_proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ota_proj.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_PATH + "templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ota',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # 'crispy_forms',
    # 'ajax_upload',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
