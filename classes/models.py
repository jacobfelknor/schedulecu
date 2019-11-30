from django.db import models
from schedules.models import Schedule

# Create your models here.

# Proposed changes:
"""
Split a class into two models - Class and Section
    - Can differentiate between REC/LEC/etc more
      concretely. Have a model for each kind
    
    - Keep historical data. Each time a new class
      list is released, simply append a section
      to an existing class instead of deleting
      old classes. This plays well with the FCQ
      stuff as well

    - Class Model (Generic for all types)
        department (Foreign key to department object)
        course_subject
        
    
    - Section Model (One for each type)
        class (Foreign key to the actual class object)
        credits
        section number
        start_time
        end_time
        instructor (foreign key to instructor)
        days
        session
        semester (Spring/Fall/Summer <year>)
        max_enrollment
        building_room
        campus
        schedule (Many to Many Field)
"""


class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=4)


class Class(models.Model):
    """ 
    General class model. Only one instance for each class
    """

    # Fields
    course_title = models.CharField(max_length=50)
    course_subject = models.IntegerField()
    # Relations
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="classes"
    )

    def empty_fields(self):
        empty = []
        for field in self.__dict__:
            if self.__dict__[field] == None or self.__dict__[field] == "":
                empty.append(field)
        return empty

    @property
    def has_sections(self):
        if len(self.sections.all()):
            return True
        else:
            return False


class Section(models.Model):
    """
    Specific Class instance. includes details about a general class
    """

    # Fields
    section_number = models.CharField(max_length=5)
    session = models.CharField(max_length=5)
    class_number = models.IntegerField()
    credit = models.CharField(max_length=5)
    class_component = models.CharField(max_length=10)
    start_time = models.CharField(max_length=10, null=True, blank=True)
    end_time = models.CharField(max_length=10, null=True, blank=True)
    days = models.CharField(max_length=10, null=True, blank=True)
    building_room = models.CharField(max_length=40, null=True, blank=True)
    instructor_name = models.CharField(max_length=50, null=True, blank=True)
    max_enrollment = models.IntegerField()
    campus = models.CharField(max_length=15)

    # Relations
    parent_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="sections"
    )
    schedule = models.ManyToManyField(Schedule, related_name="classes")

    def in_schedule(self, user):
        if self in user.schedule.classes.all():
            return True
        else:
            return False
