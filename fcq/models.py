from django.db import models

from classes.models import Department, Class

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
class Professor(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)


class FCQ(models.Model):
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=10)
    section = models.CharField(max_length=4)

    courseType = models.CharField(max_length=5)
    online = models.CharField(max_length=1)
    size = models.IntegerField(default=0)

    numResponses = models.IntegerField(default=0)
    challenge = models.FloatField(default=0.0)
    learned = models.FloatField(default=0.0)
    courseRating = models.FloatField(default=0.0)
    profEffect = models.FloatField(default=0.0) #effectiveness of professor
    profRating = models.FloatField(default=0.0)
    courseSD = models.FloatField(default=0.0) #stand. dev. for course rating
    profSD = models.FloatField(default=0.0) #stand. dev. for professor rating

    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="fcqs", null=True
    )
    course = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="fcqs"
    )

