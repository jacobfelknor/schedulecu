import os
import csv
import math
from django.core.management.base import BaseCommand, CommandError


class Teacher:
    def __init__(self, n):  # initiate class member (a teacher)
        self.name = n
        self.firstName = ''
        self.lastName = ''

        self.mainDepartment = ''

        self.numClasses = 0  # how many classes teacher has taught
        self.avgClassSize = 0

        self.avgInstRating = 0.0
        self.avgCourseRating = 0.0
        self.avgChallenge = 0.0

        self.courseList = []
        self.timesCourseTaught = []
        self.courseRating = []
        self.courseInstRating = []
        self.courseChallenge = []
        # stores index (line number in clean_fcq) of past classes taught
        self.classIndex = []


def createTeachers():
    teachers = []
    names = []
    classList = []
    numLine = 0
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'clean_fcq.csv')
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            index = 0
            for info in row:
                if index == 9:
                    if info not in names:  # if a class exists for the teacher
                        t = Teacher(info)
                        info = info.split(';')
                        info[1] = info[1][1:]
                        t.firstName = info[1]
                        t.lastName = info[0]
                        t.numClasses += 1
                        t.classIndex.append(numLine)
                        names.append(t.name)
                        teachers.append(t)
                    else:
                        t = teachers[names.index(info)]
                        t.numClasses += 1
                        t.classIndex.append(numLine)
                index += 1
            numLine += 1
    return teachers  # creates teacher object


def fillInfo(teachers):  # fills avg rating, main subject, and num semesters
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'clean_fcq.csv')
    file = open(filename)
    classFile = file.readlines()
    for t in teachers:
        classSize = 0
        t.numClasses = len(t.classIndex)
        dep = []
        depCount = []
        courses = []
        timesTaught = []
        instAvg = []
        classRating = []
        classChallenge = []
        for i in t.classIndex:
            line = classFile[i].replace('\n', '')
            line = classFile[i].split(',')

            # fills in lists with values we will use
            # --------------------------------------
            if line[5] not in dep:
                dep.append(line[5])
                depCount.append(1)
            else:
                depCount[dep.index(line[5])] += 1
            if (line[5]+' '+line[6]) not in courses:
                courses.append(line[5]+' '+line[6])
                timesTaught.append(1)
                instAvg.append(round(float(line[25]), 2))
                classRating.append(round(float(line[21]), 2))
                classChallenge.append(round(float(line[19]), 2))
            else:
                i = courses.index(line[5]+' '+line[6])
                timesTaught[i] += 1
                instAvg[i] += float(line[25])
                classRating[i] += float(line[21])
                classChallenge[i] += float(line[19])
            classSize += int(line[15])

        # calculate avg values
        # --------------------
        totalInstAvg = float(sum(instAvg)/t.numClasses)
        totalCourseRating = float(sum(classRating)/t.numClasses)
        totalChallenge = float(sum(classChallenge)/t.numClasses)
        avgSize = int(classSize/t.numClasses)
        for i in range(len(courses)):
            instAvg[i] = round(instAvg[i] / timesTaught[i], 2)
            classRating[i] = round(classRating[i] / timesTaught[i], 2)
            classChallenge[i] = round(classChallenge[i] / timesTaught[i], 2)

        # update teacher variables
        # ------------------------
        i = depCount.index(max(depCount))
        t.mainDepartment = dep[i]
        t.avgClassSize = avgSize
        t.avgInstRating = round(totalInstAvg, 2)
        t.avgCourseRating = round(totalCourseRating, 2)
        t.avgChallenge = round(totalChallenge, 2)

        # update teacher object lists
        # ---------------------------
        t.courseList = courses
        t.timesCourseTaught = timesTaught
        t.courseInstRating = instAvg
        t.courseRating = classRating
        t.courseChallenge = classChallenge


def writeCSV(teachers):
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'teachers.csv')
    with open(filename, mode='w', newline='') as clean_fcq:
        writer = csv.writer(clean_fcq, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for t in teachers:
            data = []
            data.append(t.firstName)
            data.append(t.lastName)
            data.append(t.mainDepartment)
            data.append(t.numClasses)
            data.append(t.avgClassSize)
            data.append(t.avgInstRating)
            data.append(t.avgCourseRating)
            data.append(t.avgChallenge)
            data.append(t.courseList)
            data.append(t.timesCourseTaught)
            data.append(t.courseRating)
            data.append(t.courseInstRating)
            data.append(t.courseChallenge)
            data.append(t.classIndex)
            writer.writerow(data)
            count += 1


class Command(BaseCommand):
    print("Updating teachers with clead_fcq data")

    def handle(self, *args, **options):
        teachers = createTeachers()
        fillInfo(teachers)
        writeCSV(teachers)
