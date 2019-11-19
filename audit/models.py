from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from classes.models import Class


# webscrape humanities classes off classes.colorado.edu?
# I have natsci classes already
class Audit(models.Model):

    # Database
    # Each audit is made of many DegreeSection objects, does not individually hold data

    # Relation
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


# DegreeSection holds requirements for a section of the degree (i.e. nat sci, humanities, etc)
class DegreeSection(models.Model):

    # Database
    sectionName = models.CharField(max_length=40)
    creditRequirement = models.IntegerField()
    currentCredit = models.IntegerField()
    # Relation
    appliedClasses = models.ManyToManyField(
        Class, related_name="appliedClasses")
    auditId = models.ForeignKey(Audit, on_delete=models.CASCADE)


# Model to define the classes a user has completed. A new object created for each class a user has completed
class CompletedClass(models.Model):

    # Database
    completedClass = models.CharField(max_length=10)
    # Relation
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


# Model to define the prerequisites for taking a class. ArrayField allows for multiple possible prereqs
# RequiredNumber allows defining how many need to be taken (i.e. take 6 of the following)
class Prerequisite(models.Model):

    # Database
    requiredNumber = models.IntegerField()
    possibleClasses = ArrayField(models.CharField(max_length=10),)
    # Relation. Each prereq has a class or audit exclusive
    # classId = models.ForeignKey(
    #    Class, on_delete=models.CASCADE, blank=True, null=True)
    # I believe this is many-to-many, as there are many CSCI1300 and many CSCI2270, any 1300 is a prereq for any 2270
    classes = models.ManyToManyField(Class, related_name="classes")
    auditId = models.ForeignKey(
        Audit, on_delete=models.CASCADE, blank=True, null=True)
