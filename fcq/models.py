from django.contrib.postgres.fields import ArrayField
from django.db import models

from classes.models import Department


# Proposed changes:
"""
have course rating, times taught, intructor
rating, and course challenge in the FCQ Table
instead of being array fields in the Teacher
Table. 

Foreign key back to the professor which coresponds
with the FCQ.

Change department and course to Foreign Keys
to their respective models
(this is dependent on the database changes
happening for the class models, see notes there.
If that doesn't happen, leave these as Chars)

"""


class Teacher(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    mainDepartment = models.CharField(max_length=50)
    numClasses = models.IntegerField()
    avgClassSize = models.IntegerField()
    avgInstRating = models.FloatField()
    avgCourseRating = models.FloatField()
    avgChallenge = models.FloatField()
    courseList = ArrayField(models.CharField(max_length=50))
    timesCourseTaught = ArrayField(models.IntegerField())
    courseRating = ArrayField(models.FloatField())
    courseInstRating = ArrayField(models.FloatField())
    courseChallenge = ArrayField(models.FloatField())
    classIndex = ArrayField(models.IntegerField())


class FCQ(models.Model):
    index = models.IntegerField()
    year = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    courseTitle = models.CharField(max_length=200)
    courseType = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    online = models.CharField(max_length=50)
    size = models.IntegerField()

