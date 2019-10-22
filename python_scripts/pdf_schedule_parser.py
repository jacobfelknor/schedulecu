import PyPDF2
import re
from itertools import combinations

from timeit import default_timer as timer

class Course:

    print_format = "{:<15}" * 2
    print_headers = ["Department", "Course Subject", "Section Number", "Session", "Class Number", \
        "Credit", "Course Title", "Class Component", "Start Time", "End Time", "Days", "Building Room", \
        "Instructor", "Max Enrollment", "Campus"]

    # Constructor. Saving data and each item specifically
    def __init__(self, data):
        self.department = data[0]
        self.course_subject = data[1]
        self.section_number = data[2]
        self.session = data[3]
        self.class_number = data[4]
        self.credit = data[5]
        self.course_title = data[6]
        self.class_component = data[7]
        self.start_time = data[8]
        self.end_time = data[9]
        self.days = data[10]
        self.building_room = data[11]
        self.instructor_name = data[12]
        self.max_enroll = data[13]
        self.campus = data[14]
        self.data = data

    # String conversion for printing
    def __str__(self):
        output = ""
        for i in range(len(self.print_headers)):
            output += self.print_format.format(self.print_headers[i], *self.data[i]) + '\n'
        return output



pdf_doc = open('fall2019class_schedule.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_doc)
pdf_pages = pdf_reader.pages

#pdf_reader.numPages for number of pages
#pdf_reader.outlines gives titles and I think page numbers for departments
# looks like outlines separates into colleges and departments nicely
# every even number is a college, odd numbers breaks into departments
#pdf_reader.namedDestinations draws a blank
#pagelayout is blank, pageMode is /useOutlines (idk what that means)
#pdf_reader.pages gives a list of the pages to enumerate through
#xmpMetadata might have some usable information
#xmpMetadata:
#   no pdf_keywords
#   no custom_properties
#   I don't think xmp has anything usable :(

#extractText() from pages is pretty good, each column seems to be
# separated by a newline char.
# If I define the number of columns and have something to line up
# classes with, it'll be pretty easy.

#Above in tandem with outlines, I think I can design a parser
# that is capable of separating classes into college. Or I can
# just use the text and use the class code to define.

#I can merge pages together (pages between header and next header)
# and then filter out the outside info,
# then scan to grab all the classes.
# (have to cut off text at bottom and top of pages to merge correctly)

#Departments separate by undergrad and then grad

#Also have to deal with classes with missing info (e.g. instructor)
# does not skip lines for missing info, have to detect when a column is missing
# Find which information is required to appear, find patterns in missing info
# use patterns to detect which piece is missing
# easy to find misalign with "campus" column


# -------------------------STEPS TO TAKE --------------------
# Step 1:
#     Get pages to combine nicely (erase extra data)
#     Combine pages with overlapping data
#     Remove headers, footers, and outside info
# Step 2:
#     Design parsing method


#print(pdf_reader.numPages)
#print(pdf_reader.outlines)
#print(pdf_pages[1].extractText())


#Extracts the raw text from a page.
#Removes whitespace elements
#Removes trailing space on each line
def extract_text(raw_page):
    return [x[0:len(x) - 1] for x in raw_page.extractText().split('\n') if x.strip()]

#Removes the generic header and footer from pages.
#Will not work on pages with a specific class section header
# on the top
def remove_header_footer(extracted_text):
    #Extracting class code from 0th element of extracted text
    strip = extracted_text[0].strip()
    extracted_text[0] = strip[len(strip) - 4:]
    #Removing generic footer
    del extracted_text[len(extracted_text) - 3:]

# Outlines can be used for headers to organize
#print(pdf_reader.outlines[0]['/Title'])


extr = extract_text(pdf_pages[3])
#for i in range(10):
#    extr = extract_text(pdf_pages[i + 2])
#    print((extr[0], extr[len(extr) - 4:len(extr)]))
remove_header_footer(extr)

#print(extr)

def combine_pages(page1, page2):
    pass

# Generating all possible weekday codes
weekdays = ["M", "T", "W", "TH", "F"]
weekday_list = []
for i in range(1, len(weekdays) + 1):
    weekday_list += [''.join(x) for x in combinations(weekdays, i)]

# Raw row pulled from below loop
# Parses the information in a raw row and creates a class object. 
# Complains about any error in the process
def create_course(raw_row):

    start = timer()

    class_data = []
    # Less than 5 means I can't guarentee I have all the required data
    if len(raw_row) < 5:
        print("Really bad row")
        return -1
    # Add class code and course subject
    class_data += [x for x in raw_row[0:2]]
    section_session_number_split = raw_row[2].split(" ")
    if len(section_session_number_split) != 3:
        print("Weird section_session_number split")
        print(raw_row)
        return -1
    # Add section, session, and class number
    class_data += [x for x in section_session_number_split]

    credit_title_split = raw_row[3].split(" ", 1)
    try:
        int(credit_title_split[0])
    except:
        print("Credit found as not an integer")
        print(credit_title_split)
        return -1
    
    # Add credit and class title
    class_data += [x for x in credit_title_split]
    # Add class component
    class_data += [raw_row[4]]

    # These components are not required, using Regex to find them
    raw_row_data = " ".join(raw_row[5:])
    # Pull out class time
    full_time = re.search("[0-9]{2}:[0-9]{2} [PA][M] - [0-9]{2}:[0-9]{2} [PA][M]", raw_row_data)
    if full_time == None:
        # This is expected to happen in quite a few cases
        print("No class time found")
        class_data += [""]
        class_data += [""]
    else:
        class_data += [full_time.group()[:8]]
        class_data += [full_time.group()[11:]]

    #for elem in raw_row_data.split(" "):
    day_index = 0
    for elem, day_index in zip(raw_row, range(len(raw_row))):
        if elem in weekday_list:
            class_data += [elem]
            break
    else:
        print("No days found")
        class_data += [""]
    
    # Using day to align the building column
    if day_index < len(raw_row):
        class_data += [raw_row[day_index + 1]]
    else:
        print("No building as no day, other logic needed")
    
    # All instructors have a comma in their name
    for elem in raw_row_data.split(" "):
        if ',' in elem:
            class_data += [elem]
            break
    else:
        print("No instructor found")
        class_data += [""]
    
    enrollment_campus_split = raw_row[-1].split(" ", 1)
    # Check enrollment is an integer
    try:
        int(enrollment_campus_split[0])
    except:
        print("Max enrollment is not an int")
        print(enrollment_campus_split)
    
    class_data += [enrollment_campus_split[0]]
    class_data += [enrollment_campus_split[1]]

    print(raw_row)
    print(class_data)
    # ...
    end = timer()
    print(end - start) 



#Pull out 13 elements, split last two into max enrollment and campus
def parse_rows(ext_page):
    rows = []
    index = 0
    loop = 1
    while loop:
        cur_row = ext_page[index:index + 13]
        for i in range(len(cur_row)):
            if "Main Campus" in cur_row[i]:
                adj_row = cur_row[:i + 1]
                index += i + 1
                rows += [adj_row]
                #logic to handle row
                break
        else:
            #irregular row found, need logic to handle this and swap to next dept/college
            loop = 0
    return rows

testrow = parse_rows(extr)[0]
create_course(testrow)
#print(extr[:13])
#print(adj_row)


# Row logic
# 0: Class code  'APPM'
# 1: Course subject   '3310'
# 2: Section number, session, and class number (space separated) '001 B 20735'
# 3: Credit and Course Title '3 Chaos in Dynamical Systems'
# 4: Class component 'Lec'
# 5: (USUALLY) time '12:00 PM - 12:50 PM'
# Followed by days, building/room, professor, enrollment, campus

# take len to know if its a little fucky
# kinda changes from page to page so 
# 10 means its working right
# 9 probably means no professor

# First 8 components always required
# inconsistent with/after meeting time