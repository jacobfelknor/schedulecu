import csv
import math

class Teacher:
	def __init__(self, n): #initiate class member (a teacher)
		self.name = n

		self.mainDepartment = ''

		self.numClasses = 0 #how many classes teacher has taught		
		self.avgClassSize = 0

		self.avgInstRating = 0.0
		self.avgCourseRating = 0.0
		self.avgChallenge = 0.0

		self.courseList = []
		self.timesCourseTaught = []
		self.courseRating = []
		self.courseInstRating = []
		self.courseChallenge = [] 
		self.classIndex = [] #stores index (line number in clean_fcq) of past classes taught



def createTeachers():
	teachers = []
	names = []
	classList = []
	numLine = 0
	with open('clean_fcq.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			index = 0
			for info in row:
				if index == 9:
					if info not in names: #if a class exists for the teacher
						t = Teacher(info)
						t.numClasses += 1
						t.classIndex.append(numLine)
						names.append(info)
						teachers.append(t)
					else:
						t = teachers[names.index(info)]
						t.numClasses += 1
						t.classIndex.append(numLine)
				index += 1
			numLine += 1
	return teachers #creates teacher object 



def fillInfo(teachers): #fills avg rating, main subject, and num semesters
	file = open('clean_fcq.csv')
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
			line = classFile[i].replace('\n','')
			line = classFile[i].split(',')

			#fills in lists with values we will use
			#--------------------------------------
			if line[4] not in dep:
				dep.append(line[4]) 
				depCount.append(1)
			else:
				depCount[dep.index(line[4])] += 1
			if (line[5]+line[6]) not in courses:
				courses.append(line[5]+line[6])
				timesTaught.append(1) 
				instAvg.append(float(line[25]))
				classRating.append(float(line[21]))
				classChallenge.append(float(line[19]))
			else:
				i = courses.index(line[5]+line[6])
				timesTaught[i] += 1
				instAvg[i] += float(line[25])
				classRating[i] += float(line[21])
				classChallenge[i] += float(line[19])
			classSize += int(line[15])

		#calculate avg values
		#--------------------
		totalInstAvg = float(sum(instAvg)/t.numClasses)
		totalCourseRating = float(sum(classRating)/t.numClasses)
		totalChallenge = float(sum(classChallenge)/t.numClasses)
		avgSize = int(classSize/t.numClasses)
		for i in range(len(courses)):
			instAvg[i] = instAvg[i] / timesTaught[i]
			classRating[i] = classRating[i] / timesTaught[i]
			classChallenge[i] = classChallenge[i]/timesTaught[i]

		#update teacher variables
		#------------------------
		i = depCount.index(max(depCount))
		t.mainDepartment = dep[i]
		t.avgClassSize = avgSize
		t.avgInstRating = totalInstAvg
		t.avgCourseRating = totalCourseRating
		t.avgChallenge = totalChallenge

		#update teacher object lists
		#---------------------------
		t.courseList = courses
		t.timesCourseTaught = timesTaught
		t.courseInstRating = instAvg
		t.courseRating = classRating
		t.courseChallenge = classChallenge



def writeCSV(teachers):
	with open('teachers.csv', mode='w', newline = '') as clean_fcq:
		writer = csv.writer(clean_fcq, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		count = 0
		for t in teachers:
			data = []
			data.append(t.name)
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



def main():
	teachers = createTeachers()
	fillInfo(teachers)
	writeCSV(teachers)



main()

