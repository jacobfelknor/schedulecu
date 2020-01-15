from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings
import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=13, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    major = models.CharField(max_length=15)

    def get_absolute_url(self):
        return reverse("users:view_profile", args=(self.username,))

    def empty_fields(self):
        empty = []
        for field in self.__dict__:
            if self.__dict__[field] == None or self.__dict__[field] == "":
                empty.append(field)
        return empty



def validate_file(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def update_filename(instance, filename):
    path = "documents/"
    format = "audit"
    return os.path.join(path, format)


class Document(models.Model):
    document = models.FileField(upload_to=update_filename, validators=[validate_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.document.name))
        super(Document,self).delete(*args,**kwargs)