from django.db import models
from users.models import User

# Create your models here.


class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def is_empty(self):
        if len(self.classes.all()) == 0:
            return True
        else:
            return False
