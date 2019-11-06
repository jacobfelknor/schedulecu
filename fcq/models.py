from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

# Print helpers
print_format = "{:<15}" * 2

class Teacher(models.Model):
	name = models.CharField(max_length=50)
	mainDepartment = models.CharField(max_length=6)
	numClasses = models.IntegerField(default=0)
	avgClassSize = models.IntegerField(default=0)
	avgInstRating = models.FloatField(default=0.0)
	avgCourseRating = models.FloatField(default=0.0)
	avgChallenge = models.FloatField(default=0.0)
	courseList = ArrayField(models.CharField(max_length=8),size=numClasses,)
	timesCourseTaught = ArrayField(models.IntegerField(default=1),size=numClasses,)
	courseRating = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	courseInstRating = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	courseChallenge = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	classIndex = ArrayField(models.IntegerField(),size=numClasses,)

	def __str__(self):
		output = ""
		for field in self.__dict__:
			output += print_format.format(field, *self.__dict__[field])
		return output

	def empty_fields(self):
		empty = []
		for field in self.__dict__:
			if self.__dict__[field] == None or self.__dict__[field] == "":
				empty.append(field)
		return empty


class FCQ(models.Model):
	name = models.CharField(max_length=50)
	mainDepartment = models.CharField(max_length=6)
	numClasses = models.IntegerField(default=0)
	avgClassSize = models.IntegerField(default=0)
	avgInstRating = models.FloatField(default=0.0)
	avgCourseRating = models.FloatField(default=0.0)
	avgChallenge = models.FloatField(default=0.0)
	courseList = ArrayField(models.CharField(max_length=8),size=numClasses,)
	timesCourseTaught = ArrayField(models.IntegerField(default=1),size=numClasses,)
	courseRating = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	courseInstRating = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	courseChallenge = ArrayField(models.FloatField(default=0.0),size=numClasses,)
	classIndex = ArrayField(models.IntegerField(),size=numClasses,)

	def __str__(self):
		output = ""
		for field in self.__dict__:
			output += print_format.format(field, *self.__dict__[field])
		return output

	def empty_fields(self):
		empty = []
		for field in self.__dict__:
			if self.__dict__[field] == None or self.__dict__[field] == "":
				empty.append(field)
		return empty