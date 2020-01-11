from django.db import models

from users.models import User
from classes.models import Class


# Model to define the classes a user has completed. Essentially a copy of schedule
class UserAuditEntry(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="useraudits")
	course = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="useraudits")
	year = models.CharField(max_length=10)
	semester = models.CharField(max_length=10)
	grade = models.CharField(max_length=10)