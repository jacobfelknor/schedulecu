from courses.models import Class

f = open('class_schedule.csv', 'r')

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
    course.start_time = data[7]
    course.end_time = data[8]
    course.days = data[9]
    course.building_room = data[10]
    course.instructor_name = data[11]
    course.max_enrollment = data[12]
    course.campus = data[13]
    course.save()

