import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from fcq.models import Teacher, FCQ

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
        fcq.department = data[4]
        fcq.subject = data[5]
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
    print("Failed to add" , failures, "fcq")



def PopulateTeachers():
    Teacher.objects.all().delete()

    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'teachers.csv')
    f = open(filename, 'r')

    failures = 0

    for line in f:
        teacher = Teacher()
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[:len(line) - 1].split(",")]
        teacher.firstName = data[0]
        teacher.lastName = data[1]
        teacher.mainDepartment = data[2]
        teacher.numClasses = data[3]
        teacher.avgClassSize = data[4]
        teacher.avgInstRating = data[5]
        teacher.avgCourseRating = data[6]
        teacher.avgChallenge = data[7]
        index = 8

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(data[index])
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(data[index])
        index += 1
        teacher.courseList = holder

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(int(data[index]))
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(int(data[index]))
        index += 1
        teacher.timesCourseTaught = holder

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(float(data[index]))
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(float(data[index]))
        index += 1
        teacher.courseRating = holder

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(float(data[index]))
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(float(data[index]))
        index += 1
        teacher.courseInstRating = holder

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(float(data[index]))
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(float(data[index]))
        index += 1
        teacher.courseChallenge = holder

        holder = []
        if '[' in data[index]:
            data[index] = data[index].replace('"','')
            data[index] = data[index].replace('[','')
            while index != 0:
                data[index] = data[index].replace('"','')
                data[index] = data[index].replace(' ','')

                if ']' in data[index]:
                    break
                else:
                    holder.append(int(data[index]))
                index += 1
        data[index] = data[index].replace(']','')
        holder.append(int(data[index]))
        index += 1
        teacher.classIndex = holder
        try:
            with transaction.atomic():
                teacher.save()
        except:
            print(data)
            failures += 1
    print("Failed to add" , failures, "classes")


class Command(BaseCommand):
    print("Updating fcq'a with clean_fcq.csv found in fcq/management/commands")
    def handle(self, *args, **options):
        PopulateFCQ()
        PopulateTeachers()