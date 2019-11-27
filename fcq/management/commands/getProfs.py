import os
import csv
import math
from django.core.management.base import BaseCommand, CommandError


class Professor:
    def __init__(self, n):  # initiate class member (a teacher)
        self.fullName = n
        self.firstName = ''
        self.lastName = ''

def getProfessors():
    professors = []
    names = []
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'clean_fcq.csv')
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            index = 0
            for info in row:
                if index == 9:
                    if info not in names:  # if a class exists for the teacher
                        p = Professor(info)
                        info = info.split(';')
                        info[1] = info[1][1:]
                        p.firstName = info[1]
                        p.lastName = info[0]
                        names.append(p.fullName)
                        professors.append(p)
                index += 1
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'professors.csv')
    with open(filename, mode='w', newline='') as clean_fcq:
        writer = csv.writer(clean_fcq, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for p in professors:
            data = []
            data.append(p.fullName)
            data.append(p.lastName)
            data.append(p.firstName)
            writer.writerow(data)

class Command(BaseCommand):
    print("Getting list of unique CU Professors...")
    def handle(self, *args, **kwargs):
        # Return values are for tests. test kwarg flag will be set if used with test
        in_test = kwargs.pop("test", False)
        if in_test:
            if getProfessors():
                return True
            else:
                return False
        else:
            getProfessors()
