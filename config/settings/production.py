from .development import *

DEBUG = False

DATABASES = {
    # production database configuration
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "schedulecu$schedulecu",
        "USER": "schedulecu",
        "PASSWORD": db_password,
        "HOST": "schedulecu.mysql.pythonanywhere-services.com",
    }
}

ALLOWED_HOSTS.append("schedulecu.pythonanywhere.com")

