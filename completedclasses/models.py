from django.db import models
from users.models import User


# Model to define the classes a user has completed. Essentially a copy of schedule
class CompletedClasses(models.Model):
    # Relation
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="completed")
