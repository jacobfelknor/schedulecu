from django.db import models

# Create your models here.

# Print helpers
print_format = "{:<15}" * 2


class Class(models.Model):

    # Database
    department = models.CharField(max_length=4)
    course_subject = models.IntegerField()
    section_number = models.CharField(max_length=5)
    session = models.CharField(max_length=5)
    class_number = models.IntegerField()
    credit = models.CharField(max_length=5)
    course_title = models.CharField(max_length=50)
    class_component = models.CharField(max_length=10)
    start_time = models.CharField(max_length=10, null=True, blank=True)
    end_time = models.CharField(max_length=10, null=True, blank=True)
    days = models.CharField(max_length=10, null=True, blank=True)
    building_room = models.CharField(max_length=40, null=True, blank=True)
    instructor_name = models.CharField(max_length=50, null=True, blank=True)
    max_enrollment = models.IntegerField()
    campus = models.CharField(max_length=15)
    """
    def __str__(self):
        output = ""
        for field in self.__dict__:
            output += print_format.format(field, *self.__dict__[field])
        return output
    """
    def empty_fields(self):
        empty = []
        for field in self.__dict__:
            if self.__dict__[field] == None or self.__dict__[field] == "":
                empty.append(field)
        return empty

