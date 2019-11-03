from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from classes.models import Class

def PopulateClasses():
    Class.objects.all().delete()

    f = open('classes/management/commands/class_schedule.csv', 'r')

    failures = 0

    for line in f:
        course = Class()
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[:len(line) - 1].split(",")]
        course.department = data[0]
        course.course_subject = data[1]
        course.section_number = data[2]
        course.session = data[3]
        course.class_number = data[4]
        course.credit = data[5]
        course.course_title = data[6]
        course.class_component = data[7]
        course.start_time = data[8]
        course.end_time = data[9]
        course.days = data[10]
        course.building_room = data[11]
        course.instructor_name = data[12]
        course.max_enrollment = data[13]
        course.campus = data[14]
        try:
            with transaction.atomic():
                course.save()
        except:
            print(data)
            failures += 1
    print("Failed to add" , failures, "classes")

class Command(BaseCommand):
    def handle(self, *args, **options):
        PopulateClasses()