from django.db import models
from classes.models import Class
from audit.models import Audit


# Model to hold natsci classes and current credit to
class NatSciRequirement(models.Model):

    # Database
    creditRequirement = models.IntegerField()
    currentCredit = models.IntegerField()
    # Relation
    auditId = models.ForeignKey(Audit, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class, related_name="classes")
