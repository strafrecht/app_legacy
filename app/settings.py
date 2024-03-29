"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

#sentry_sdk.init(
#    dsn="https://b43678e42cdf4f38a9b0dadf573da567@o244196.ingest.sentry.io/1723408",
#    integrations=[DjangoIntegration()],
#    traces_sample_rate=1.0, # We recommend lowering this in production

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
#    send_default_pii=True
#)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#g*o!3=v$8+ag9%^&llf6h-fhm9zsrjlmb+s0)g&#*b1*8l##w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'bd3b44d2f1b0.ngrok.io',
    'app',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition
CELERY_BROKER_URL = 'redis://localhost:6379/0'


INSTALLED_APPS = [
    # Live Reload
    #'livereload',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin Interface
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'pagedown',
    'django_filters',
    'debug_toolbar',

    # Assets
    'pipeline',
    'pwa',

    # Pages
    'app',
    'core',
    'pages',
    'news',
    #'emails',
    'profiles',
    #'leaflet',
    'feedback',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtailcolumnblocks',
    'wagtail_color_panel',
    'wagtailfontawesome',

    'modelcluster',
    'taggit',

    # Wiki
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.editsection.apps.EditSectionConfig',
    'wiki.plugins.help.apps.HelpConfig',
    'wiki.plugins.links.apps.LinksConfig',
    'wiki.plugins.globalhistory.apps.GlobalHistoryConfig',
    'editors',
    'markdownify',

    # Chatter
    #'django_chatter',

    # User Profile
    'avatar',

    # Comments
    'django_comments_xtd',
    'django_comments',
    'comments_wagtail_xtd',

    # Wagtail News
    'wagtailnews',

    # Wagtail Menus
    'wagtailmenus',

    # Wagtail Newsletter
    #'mjml',
    #'birdsong',

    # Link Checker
    #'wagtaillinkchecker',

    # Wagtail Polls
    'wagtailpolls',
    'wagtail.contrib.modeladmin',

    # DRF
    'rest_framework',
    'rest_framework.authtoken',

    # cors-headers
    'corsheaders',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    #'livereload.middleware.LiveReloadScript',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

#WSGI_APPLICATION = 'wsgi.application'
ASGI_APPLICATION = 'app.routing.application'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.yourserver.com'
    EMAIL_PORT = '<your-server-port>'
    EMAIL_HOST_USER = 'your@djangoapp.com'
    EMAIL_HOST_PASSWORD = 'your-email account-password'
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'NAME': 'django_tests',
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

CHANNEL_LAYERS = {
  'default': {
      'BACKEND': 'channels_redis.core.RedisChannelLayer',
      'CONFIG': {
        'hosts': [('127.0.0.1', 6379)],
      },
  },
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'pipeline.storage.PipelineManifestStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/build')
]

WAGTAIL_SITE_NAME = 'strafrecht-online'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SITE_ID = 1

PIPELINE = {
    'PIPELINE_ENABLED': False, #not DEBUG
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
        'pipeline.compilers.es6.ES6Compiler'
    ),
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    #'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'BABEL_ARGUMENTS': '', #'--presets es2016',
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'css/base.css',
                'css/bootstrap.css',
                'css/charts.css'
                'css/mysite.css',
                'css/content.css',
                'css/navbar.css',
                'css/custom-wagtail-columns.css'
                'css/sidebar.css',
                'css/wiki.css',
                'css/comments.css',
            ),
            'output_filename': 'css/main.css',
        },
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
                'js/index.js',
                #'js/mysite.js',
                #'js/editor.js',
                #'js/chartist.js',
                #'js/chartist-plugin-fill-donut.js',
            ),
            'output_filename': 'js/index.js'
        },
        'vendor': {
            'source_filenames': (
                'tui-editor'
            ),
            'output_filename': 'js/vendor.js',
        }
    }
}

X_FRAME_OPTIONS='SAMEORIGIN'

WIKI_ACCOUNT_HANDLING = True
WIKI_ACCOUNT_SIGNUP_ALLOWED = True
WIKI_ANONYMOUS = True
WIKI_ANONYMOUS_CREATE = True
WIKI_ANONYMOUS_WRITE = True
WIKI_EDITOR = 'editors.modern.Modern'
WIKI_CHECK_SLUG_URL_AVAILABLE = False

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
COMMENTS_XTD_CONFIRM_EMAIL = False

CHAT_WS_SERVER_HOST = 'localhost'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'

#import os
#if os.name == 'nt':
#    import platform
#    OSGEO4W = r"C:\OSGeo4W"
#    if '64' in platform.architecture()[0]:
#        OSGEO4W += "64"
#    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
#    os.environ['OSGEO4W_ROOT'] = OSGEO4W
#    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
#    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
#else:
#    GDAL_LIBRARY_PATH = '/usr/include/gdal'

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://127.0.0.1:8000"
# ]


CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
}

PWA_APP_NAME = 'Strafrecht Online'
PWA_APP_DESCRIPTION = "Strafrecht Online"
PWA_APP_THEME_COLOR = 'rgb(76, 158, 187)'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icon.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

AVATAR_GRAVATAR_DEFAULT = 'identicon'
AVATAR_EXPOSE_USERNAMES = False
AVATAR_MAX_AVATARS_PER_USER = '1'

# CSP_SCRIPT_SRC = ("'self'", "'unsafe-eval'", "'unsafe-inline'",)
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
