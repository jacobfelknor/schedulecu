from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from audit.models import Prerequisite
from classes.models import Class, Department, Section


def PopulatePrereqs():
    file = open("audit/requirements/prerequisites/prereqs.csv", "r")
    prereqFailures = []
    for line in file:
        line = line.split(",")
        departCode = line[0][:4]
        classNumber = line[0][4:]
        prereq = Prerequisite()
        try:
            prereq.classes = Class.objects.filter(
                course_subject=classNumber).filter(department__code=departCode).get()
            prereq.requiredNumber = int(line[1])
            prereq.corequisite = line[2]

            with transaction.atomic():
                prereq.save()

            # The prereqs.csv file is a mess
            # I'd rather write python to parse it than manually change it
            appliedClassNames = [y.replace(" ", "") for x in line[3:]
                                 for y in x.split("or")]
            # chop off newline
            appliedClassNames[-1] = appliedClassNames[-1][:-1]

            for name in appliedClassNames:
                departCode = name[:4]
                classNumber = name[4:]
                try:
                    prereq.possibleClasses.add(Class.objects.filter(
                        course_subject=int(classNumber)).filter(department__code=departCode).get())
                except:
                    prereqFailures += [name]
        except:
            print("Unable to find class: {}".format(line[0]))
    if len(prereqFailures) > 0:
        print("Failed to add the following classes as prereqs: \n",
              list(set(prereqFailures)))
        print(
            "A number of failures is expected as not every class is offered every semester")


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Populating Prerequisites from audit/requirements/prerequisites/prereqs.csv")
        Prerequisite.objects.filter(audit=None).delete()
        PopulatePrereqs()
