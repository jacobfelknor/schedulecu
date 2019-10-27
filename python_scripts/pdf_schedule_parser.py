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
        for elem in data:
            output += str(elem).replace(",", ";") + ","
        #for i in range(len(self.print_headers)):
        #    output += self.print_format.format(self.print_headers[i], *self.data[i]) + '\n'
        return output[:len(output) - 1]



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

# Helper functions and otherwise

def is_int(str_input):
    try:
        int(str_input)
        return True
    except:
        return False

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
def has_numbers(str_input):
    for number in numbers:
        if number in str_input:
            return False
    return True

# Generating all possible weekday codes
weekdays = ["M", "T", "W", "TH", "F"]
weekday_list = []
for i in range(1, len(weekdays) + 1):
    weekday_list += [''.join(x) for x in combinations(weekdays, i)]
weekday_list += ["TBA"]

class_components = ["SEM", "LEC", "REC", "STU", "WKS", "MLS", "LAB", "PRA", "FLD", "CLN"]

# GRE and MUS duplicate keys
department_codes = {
    "ANTH" : 1,
    "APPM" : 1,
    "ARAB" : 1,
    "ARTF" : 1,
    "ARTH" : 1,
    "ARTS" : 1,
    "ARSC" : 1,
    "ASIA" : 1,
    "ASTR" : 1,
    "ATOC" : 1,
    "CWC" : 1,
    "CHE" : 1,
    "CAM" : 1,
    "CHIN" : 1,
    "CLAS" : 1,
    "DNC" : 1,
    "EBIO" : 1,
    "ECO" : 1,
    "ENGL" : 1,
    "ENVS" : 1,
    "ETHN" : 1,
    "FRSI" : 1,
    "FREN" : 1,
    "GEO" : 1,
    "GEOL" : 1,
    "GRM" : 1,
    "GSLL" : 1,
    "HEBR" : 1,
    "HIND" : 1,
    "HIST" : 1,
    "HON" : 1,
    "HUM" : 1,
    "INDO" : 1,
    "IPHY" : 1,
    "IAFS": 1,
    "ITAL": 1,
    "JPNS" : 1,
    "JWST" : 1,
    "KREN" : 1,
    "LGBT" : 1,
    "LIBB" : 1,
    "LING" : 1,
    "MATH" : 1,
    "MEM" : 1,
    "MCD" : 1,
    "MUS" : 1,
    "NRS" : 1,
    "PACS" : 1,
    "PHIL" : 1,
    "PHYS" : 1,
    "PSCI" : 1,
    "PORT" : 1,
    "PSYC" : 1,
    "RLST" : 1,
    "RUSS" : 1,
    "SCAN" : 1,
    "SOCY" : 1,
    "SPAN" : 1,
    "SLHS" : 1,
    "SWE" : 1,
    "THTR" : 1,
    "WRT" : 1,
    "ASEN" : 1,
    "AREN" : 1,
    "ATLS" : 1,
    "CVEN" : 1,
    "CSCI" : 1,
    "ECEN" : 1,
    "EHO" : 1,
    "EME" : 1,
    "EVEN" : 1,
    "GRE" : 1,
    "HUE" : 1,
    "MCE" : 1,
    "TLEN" : 1,
    "APRD" : 1,
    "COM" : 1,
    "CMD" : 1,
    "INFO" : 1,
    "JRNL" : 1,
    "MDST" : 1,
    "CMCI" : 1,
    "MUEL" : 1,
    "EMU" : 1,
    "PMU" : 1,
    "TMUS" : 1,
    "AIRR" : 1,
    "MILR" : 1,
    "NAVR" : 1,
    "PRLC" : 1,
    "ACCT" : 1,
    "BAD" : 1,
    "BCO" : 1,
    "BSL" : 1,
    "CSER" : 1,
    "ESBM" : 1,
    "FNCE" : 1,
    "INBU" : 1,
    "MGM" : 1,
    "MKT" : 1,
    "MBAX" : 1,
    "MBA" : 1,
    "MSB" : 1,
    "MSBX" : 1, 
    "ORM" : 1,
    "REAL" : 1,
    "ARC" : 1,
    "ENVD" : 1,
    "EDU" : 1,
    "LEAD" : 1,
    "LAW": 1,
}

# Raw row pulled from below loop
# Parses the information in a raw row and creates a class object. 
# Complains about any error in the process
def create_course(raw_row):

    #start = timer()
    # Beginning at 2 since the 0 and 1 element are guarenteed
    data_iterator = 2

    class_data = []
    # Less than 5 means I can't guarentee I have all the required data
    if len(raw_row) < 5:
        print("Really bad row")
        print(raw_row)
        return 1

    # Add class code and course subject
    # Grabs everything up to class 

    flattened_subdata = [y for x in raw_row for y in x.split()]
    class_data += [x for x in flattened_subdata[:6]]

    
    # Might want a dictionary with class types, will make pulling class name easier
    data_iterator = 6
    while flattened_subdata[data_iterator] not in class_components:
        data_iterator += 1
        if (data_iterator >= len(flattened_subdata)):
            data_iterator = 6
            break
    if data_iterator == 6:
        print("Unable to find class name (i.e. maybe name is len(3))?")
    else:
        class_data += [" ".join([x for x in flattened_subdata[6:data_iterator]])]
        class_data += [flattened_subdata[data_iterator]]
        data_iterator += 1
    


    # These components are not required, using Regex to find them
    #raw_row_data = " ".join(flattened_subdata[data_iterator:]).replace("-", "")
    raw_row_data = " ".join(flattened_subdata).replace("-", "")
    # Pull out class time
    full_time = re.search("[0-9]{2}:[0-9]{2} [PA][M]  [0-9]{2}:[0-9]{2} [PA][M]", raw_row_data)
    if full_time == None:
        # This is expected to happen in quite a few cases
        print("No class time found")
        print(raw_row_data)
        class_data += [""]
        class_data += [""]
    else:
        class_data += [full_time.group()[:8]]
        class_data += [full_time.group()[10:]]

    #for elem in raw_row_data.split(" "):
    day_index = 0
    #for elem, day_index in zip(raw_row, range(len(raw_row))):
    #    if elem in weekday_list:
    #        class_data += [elem]
    #        break
    for day_index in range(len(raw_row)):
        if raw_row[day_index] in weekday_list:
            class_data += [raw_row[day_index]]
            break
    else:
        # Possible day is lumped in with some other element (probably class)
        for elem in raw_row_data.split(" "):
            if elem in weekday_list:
                class_data += [elem]
                day_index = 0
                break
        else:
            # Definitely not there
            print("No days found")
            day_index = len(raw_row)
            class_data += [""]
            
    # Using day to align the building column
    # Pretty horrible coding practice here, I'm using day_index as an error code
    # to know how I found the days before to avoid declaring more variables....
    if day_index == 0:
        # Splits everything in raw_row and flattens it
        #flattened_subdata = [y for x in raw_row for y in x.split()]
        for i in range(len(flattened_subdata)):
            if class_data[-1] == flattened_subdata[i].replace("-", ""):
                # Day is probably lumped in with the class
                # Need to know if the next element is entire building and room or only the building
                if re.search("[0-9]", flattened_subdata[i + 1]) == None:
                    class_data += [flattened_subdata[i + 1] + flattened_subdata[i + 2]]
                else:
                    class_data += [flattened_subdata[i + 1]]
                break
        else:
            print("Unable to find building off day")
            class_data += [""]
    elif day_index < len(raw_row):
        class_data += [raw_row[day_index + 1]]
    else:
        class_data += [""]
        print("No building found")
    
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
        class_data += [enrollment_campus_split[0].replace("-", "")]
        class_data += [enrollment_campus_split[1]]
    except:
        # If this fails this means the enrollment is something weird. It should be req though.
        int(enrollment_campus_split[1].split()[0])
        class_data += [enrollment_campus_split[1].replace("-", "").split()[0]]
        class_data += [enrollment_campus_split[1].split()[1]]

    

    #print(raw_row)
    if (len(class_data)) != 15:
        print(class_data)
        print(flattened_subdata)
        return 1

    # fixing 'SeeClass' building / room bug
    if class_data[11] == "SeeClass":
        # See classroom notes for room
        class_data[11] = "See Classroom Notes for Room"
    elif "SeeAca" in class_data[11]:
        class_data[11] = "See Academic Dept for Room Info"

    #print(class_data)
    return 0, class_data

    #end = timer()
    #print(end - start) 



#Pull out 13 elements, split last two into max enrollment and campus
def parse_rows(ext_page):
    rows = []
    index = 0
    loop = 1
    while loop:
        cur_row = ext_page[index:index + 13]
        # Make sure we're starting on a class code, make a dictionary if this trick doesn't work
        if cur_row:
            while cur_row and department_codes.get(cur_row[0]) == None:
            #(len(cur_row[0]) > 4 or len(cur_row[0]) < 3) and not has_numbers(cur_row[0]):
                cur_row = cur_row[1:]
                index += 1

        for i in range(len(cur_row)):
            if "Main Campus" in cur_row[i]:
                adj_row = cur_row[:i + 1]
                index += i + 1
                rows += [adj_row]
                #logic to handle row
                break
        else:
            index += 13
            # Irregular row found, using "Main Campus" to align where the next row begins            
            while index < len(ext_page) and "Main Campus" not in ext_page[index]:
                index += 1

        if (index > len(ext_page)):
            loop = 0
    return rows


#extr = extract_text(pdf_pages[1])

#for i in range(10):
#    extr = extract_text(pdf_pages[i + 2])
#    print((extr[0], extr[len(extr) - 4:len(extr)]))
#remove_header_footer(extr)

#testrow = parse_rows(extr)[1]
#for row in parse_rows(extr):
#    create_course(row)


#create_course(testrow)
#print(extr[:13])
#print(adj_row)



# ---------------------- Attempting all pages --------------------- #

failed_class_counter = 0


#for page in pdf_pages[137:138]:
#for page in pdf_pages[1:2]:
f = open("class_schedule.csv", "w")

# fixing bio lab bug
page_num = 0
bio_lab_number = 6

for page in pdf_pages:
    extr = extract_text(page)
    remove_header_footer(extr)
    for row in parse_rows(extr):
        #print(row)
        # Specifically only page 26 has a weird bug where it cuts off the section number
        if page_num == 26:
            row.insert(2, str(bio_lab_number))
            bio_lab_number += 1

        failure, data = create_course(row)
        failed_class_counter += failure
        course = Course(data)
        f.write(str(course) + "\n")
    
    page_num += 1
f.close()

print("Failed", failed_class_counter, "classes")

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