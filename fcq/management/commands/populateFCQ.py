import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from fcq.models import Professor, FCQ


def PopulateFCQ():
    FCQ.objects.all().delete()
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'clean_fcq.csv')
    f = open(filename, 'r')
    failures = 0
    for line in f:
        fcq = FCQ()
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[:len(line) - 1].split(",")]
        fcq.semester = data[0]
        fcq.year = data[1]
        fcq.department = data[5]
        fcq.course = data[6]
        fcq.section = data[7]
        fcq.courseTitle = data[8]
        fcq.courseType = data[11]
        fcq.level = data[12]
        fcq.online = data[13]
        fcq.size = data[14]
        fcq.index = data[28]
        try:
            with transaction.atomic():
                fcq.save()
        except:
            print(data)
            failures += 1
    print("Failed to add", failures, "fcq")


def PopulateProfessors():
    Professor.objects.all().delete()
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'professors.csv')
    f = open(filename, 'r')
    failures = 0
    for line in f:
        professor = Professor()
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[:len(line) - 1].split(",")]
        professor.fullName = data[0]
        professor.lastName = data[1]
        professor.firstName = data[2]
        try:
            with transaction.atomic():
                professor.save()
        except:
            print(data)
            failures += 1
    print("Failed to add", failures, "professors")


class Command(BaseCommand):
    print("Filling FCQ and Professor database tables...")
    def handle(self, *args, **kwargs):
        # Return values are for tests. test kwarg flag will be set if used with test
        in_test = kwargs.pop("test", False)
        if in_test:
            if PopulateProfessors() and PopulateFCQ():
                return True
            else:
                return False
        else:
            PopulateProfessors()
            # PopulateFCQ()
