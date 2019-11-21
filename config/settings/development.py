"""
Django settings for schedulecu project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

try:
    from .keys import db_password, secret_key, email_password
except ImportError as e:
    print(
        "\n***********************************\n\nWARNING: {}. Using default configuration. This should ONLY be used by Travis for build testing.\n\n***********************************\n".format(
            e
        )
    )
    db_password = ""
    secret_key = (
        "3u57j-w!+4m_k-f1(or!1d_n4bmrwi!+a@x9xvdt^r0qs(jj@!"
    )  # NOTE: This is an alternate secret key for build testing ONLY!
    email_password = (
        ""
    )  # NOTE: no way to test sending emails, since our password is necessary.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home.apps.HomeConfig",
    "users.apps.UsersConfig",
    "classes.apps.ClassesConfig",
    "schedules.apps.SchedulesConfig",
    "crispy_forms",
    "ajax_select",
    "contact.apps.ContactConfig",
    "fcq.apps.FcqConfig",
    "audit.apps.AuditConfig",
    "completedclasses.apps.CompletedclassesConfig",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "schedulecu.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR + "/schedulecu/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "schedulecu.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "schedulecu",
        "USER": "postgres",
        "PASSWORD": db_password,
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AJAX_LOOKUP_CHANNELS = {"major": ("users.lookups", "MajorLookup")}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "scheduleCU@gmail.com"
EMAIL_HOST_PASSWORD = email_password

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    # os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "schedulecu/static/"),
    "schedulecu/static/"
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "schedulecu/media")

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "login"

LOGOUT_URL = "logout"


LOGIN_REDIRECT_URL = "home:home"

LOGOUT_REDIRECT_URL = "home:home"
