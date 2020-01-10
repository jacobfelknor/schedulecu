from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings
import os

import magic
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



@deconstructible
class FileValidator(object):
    error_messages = {
     'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, content_types=()):
        self.content_types = content_types

    def __call__(self, data):
        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = { 'content_type': content_type }
                raise ValidationError(self.error_messages['content_type'],'content_type', params)

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.content_types == other.content_types
        )


class Document(models.Model):
    validate_file = FileValidator(content_types=('application/pdf',))
    document = models.FileField(upload_to='documents/', validators=[validate_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.document.name))
        super(Document,self).delete(*args,**kwargs)