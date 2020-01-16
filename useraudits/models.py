from django.db import models

from users.models import User
from classes.models import Class, Department

# Model to define the classes a user has completed. Essentially a copy of schedule
class UserAuditEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="useraudits")
    course = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="useraudits")
    year = models.CharField(max_length=10, blank=True)
    semester = models.CharField(max_length=10, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    credits = models.FloatField(default=0.0)
    transfer = models.BooleanField(null=True)

    def has_audit(user):
        audit = UserAuditEntry.objects.filter(user=user)
        if len(audit) > 0:
            return True
        else:
            return False


class UserAuditTransferEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usertransfers")
    year = models.CharField(max_length=10, blank=True)
    semester = models.CharField(max_length=10, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="usertransfers")
    level = models.CharField(max_length=10, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    credits = models.FloatField(default=0.0)


class UserAuditInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userauditinfo")
    gpa_cu = models.FloatField(default=0.0)
    gpa_transfer = models.FloatField(default=0.0)
    gpa_complete = models.FloatField(default=0.0)
    progress = models.FloatField(default=0.0)
    attempted = models.FloatField(default=0.0)
    earned = models.FloatField(default=0.0)
    transfer_credits = models.FloatField(default=0.0)
    num_cu_courses = models.IntegerField(default=0)
    num_transfers = models.IntegerField(default=0)