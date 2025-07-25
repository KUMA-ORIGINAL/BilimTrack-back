"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(env("DEBUG", default=0))

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")

DOMAIN = env("DOMAIN")

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type", "Accept"]

if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


INSTALLED_APPS = [
    'unfold',
    "unfold.contrib.filters",
    "unfold.contrib.import_export",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'django_filters',
    'djoser',
    'corsheaders',
    'cachalot',
    'import_export',

    'account',
    'academics',
    'schedule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',

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
        'DIRS': [BASE_DIR / 'templates'],
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # Используется PostgreSQL
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN}", f"http://{DOMAIN}"]

AUTH_USER_MODEL = 'account.User'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'django': {
        'handlers': ['console'],
        'level': 'INFO',  # или DEBUG для детальных логов
    },
}


if DEBUG:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')

CACHALOT_ENABLED = True
CACHALOT_ONLY_CACHABLE_TABLES = (
    'account_achievement',
    'account_rarity',
    'account_user',
    'account_skill',
    'account_tool',

    'academics_group',
    'academics_subject',
    'academics_grade',
)
CACHALOT_TIMEOUT = 60 * 30

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'BilimTrack',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CAMELIZE_NAMES': True,

    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields',
    ],
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    'UPDATE_LAST_LOGIN': True,
}

DJOSER = {
    # 'SERIALIZERS': {
    #     'user': 'account.serializers.UserSerializer',
    #     'current_user': 'account.serializers.UserSerializer',
    # },
}

UNFOLD = {
    "SITE_TITLE": 'BilimTrack',
    "SITE_HEADER": "BilimTrack",
    "SITE_URL": "/",
    "SITE_SYMBOL": "settings",  # symbol from icon set
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Главная"),
                "items": [
                    {
                        "title": _("Учебные заведения"),
                        "icon": "domain",
                        "link": reverse_lazy("admin:academics_organization_changelist"),
                    },
                    {
                        "title": _("Оценки"),
                        "icon": "stars",
                        "link": reverse_lazy("admin:academics_grade_changelist"),
                    },
                    {
                        "title": _("Курсы"),
                        "icon": "school",
                        "link": reverse_lazy("admin:academics_course_changelist"),
                    },
                    {
                        "title": _("Группы"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:academics_group_changelist"),
                    },
                    {
                        "title": _("Предметы"),
                        "icon": "subject",
                        "link": reverse_lazy("admin:academics_subject_changelist"),
                    },
                    {
                        "title": _("Занятия"),
                        "icon": "event",
                        "link": reverse_lazy("admin:academics_session_changelist"),
                    },
                ]
            },
            {
                "title": _("Расписание"),
                "items": [
                    {
                        "title": _("Преподаватели"),
                        "icon": "person",
                        "link": lambda request: f"{reverse_lazy('admin:account_user_changelist')}?role__exact=mentor",
                    },
                    {
                        "title": _("Аудитории"),
                        "icon": "location_on",
                        "link": reverse_lazy("admin:schedule_room_changelist"),
                    },
                    {
                        "title": _("Время пар"),
                        "icon": "schedule",
                        "link": reverse_lazy("admin:schedule_lessontime_changelist"),
                    },
                    {
                        "title": _("Типы занятий"),
                        "icon": "category",
                        "link": reverse_lazy("admin:schedule_lessontype_changelist"),
                    },
                    {
                        "title": _("Занятия"),
                        "icon": "event_note",
                        "link": reverse_lazy("admin:schedule_schedule_changelist"),
                    },
                ],
            },
            {
                "title": _("Достижения"),
                "items": [
                    {
                        "title": _("Достижения"),
                        "icon": "trophy",
                        "link": reverse_lazy("admin:account_achievement_changelist"),
                    },
                    {
                        "title": _("Редкости"),
                        "icon": "category",
                        "link": reverse_lazy("admin:account_rarity_changelist"),
                    },
                    {
                        "title": _("Пользовательские достижения"),
                        "icon": "rewarded_ads",
                        "link": reverse_lazy("admin:account_userachievement_changelist"),
                    },
                ]
            },
            {
                "title": _("Пользователи"),
                "items": [
                    {
                        "title": _("Пользователи"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_user_changelist"),
                    },
                    {
                        "title": _("Технологии"),
                        "icon": "home_repair_service",
                        "link": reverse_lazy("admin:account_tool_changelist"),
                    },
                    {
                        "title": _("Навыки"),
                        "icon": "psychology",
                        "link": reverse_lazy("admin:account_skill_changelist"),
                    },
                    # {
                    #     "title": _("Группы"),
                    #     "icon": "group",
                    #     "link": reverse_lazy("admin:auth_group_changelist"),
                    #     "permission": "account.utils.permission_callback",
                    # },
                ],
            },
        ],
    },
    # "TABS": [
    #     {
    #         "models": ["venues.venue"],
    #         "items": [
    #             {
    #                 "title": "Генерация qr-code",
    #                 "icon": "grade",
    #                 "link": reverse_lazy("admin:qr"),
    #             },
    #         ],
    #     },
    # ],
}