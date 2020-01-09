import PyPDF2

course_data = []
pdf = open('csci.pdf', 'rb')
file = PyPDF2.PdfFileReader(pdf)
numPages = file.numPages
offset = len(str(numPages))
classes = False
find = False

#all classes a user has taken has been sectioned off. We just need to find the subj and course number
#to store. We also need to look for 'TC' in the name of the course to see if the credit is a transfer
#if it is a transfer, we need to find the equivalence of said course at CU.

#Parse the pdf and grab the lines of text we're interested in (classes taken, gpa, major, minor, etc)
for i in range(numPages):
	page = file.getPage(i)
	pageText = page.extractText()
	text = pageText.split(' ')
	track = False
	for j in text:
		if j[offset:] == 'Coursework':
			track = True
		elif track:
			if j[:7] == 'History':
				classes = True
			else:
				track = False
		elif classes:
			if 'TermCourseCreditsGradeTitle' in j:
				find = True
				classes = False
		if find:
			if ('SP' in j or 'SU' in j or 'FA' in j) and ('NEED' not in j) and ('999TC' not in j):
				course_data.append(j)

#change the following substrings so we correctly parse lines of text:
#	CSPB
#	LDSP
#	SPAN
#	SUST
#	FARR
#Also, parse lines at 'TermCourseCreditsGradeTitle' if said substring exists
for i in range(len(course_data)):
	if 'CSPB' in course_data[i]:
		course_data[i] = course_data[i].replace('CSPB','!!!!')
	if 'LDSP' in course_data[i]:
		course_data[i] = course_data[i].replace('LDSP','@@@@')
	if 'SPAN' in course_data[i]:
		course_data[i] = course_data[i].replace('SPAN','####')
	if 'SUST' in course_data[i]:
		course_data[i] = course_data[i].replace('SUST','$$$$')
	if 'FARR' in course_data[i]:
		course_data[i] = course_data[i].replace('FARR','&&&&')
	if 'TermCourseCreditsGradeTitle' in course_data[i]:
		course_data[i] = course_data[i].split('TermCourseCreditsGradeTitle')[1]

#clean parsed data
for i in range(len(course_data)):
	if 'SP' in course_data[i]: #handle spring course
		course_data[i] = 'SP' + course_data[i].split('SP')[1]
	if 'SU' in course_data[i]: #handle summer course
		course_data[i] = 'SU' + course_data[i].split('SU')[1]
	if 'FA' in course_data[i]: #handle fall course
		course_data[i] = 'FA' + course_data[i].split('FA')[1]
		
#finish parse and store all cleaned courses in array 
course_history = []
for i in range(len(course_data)):
	term = ''
	year = ''
	subject = ''
	courseNum = ''
	grade = ''
	holder = course_data[i][:18]

	if (holder[-1] != '-') and (holder[-1] != '+') and (holder[-1] != '*'):
		holder = holder[:-1]
	if holder[:2] == 'SP':
		term = 'Spring'
	elif holder[:2] == 'SU':
		term = 'Summer'
	elif holder[:2] == 'FA':
		term = 'Fall'

	holder = holder[2:]
	year = holder[:2]
	holder = holder[2:]
	subject = holder[:4]
	holder = holder[4:]
	courseNum = holder[:4]
	holder = holder[7:]

	holder = holder.replace('T', '')
	if holder[-1] == '*':
		grade = '*'
	elif (holder[-1] == '-') or (holder[-1] == '+'):
		grade = holder
	elif len(holder) == 1:
		grade = holder
	else:
		grade = holder[:-1]

	if subject == '!!!!':
		subject = 'CSPB'
	if subject == '@@@@':
		subject = 'LDSP'
	if subject == '####':
		subject = 'SPAN'
	if subject == '$$$$':
		subject = 'SUST'
	if subject == '&&&&':
		subject = 'FARR'

	holder = [term,year,subject,courseNum,grade]
	course_history.append(holder)

for i in course_history:
	print(i)
print(len(course_history))