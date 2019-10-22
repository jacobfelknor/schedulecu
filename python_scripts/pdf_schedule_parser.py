import PyPDF2

class Course:

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


    department = ""
    course_subject = ""
    section_number = 0
    session = ""
    class_number = 0
    credit = 0
    course_title = ""
    class_component = ""
    start_time = 0
    end_time = 0
    days = ""
    building_room = ""
    instructor_name = ""
    max_enroll = 0
    campus = ""



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


#Pull out 13 elements, split last two into max enrollment and campus
index = 0
loop = 1
while loop:
    cur_row = extr[index:index + 13]
    for i in range(len(cur_row)):
        if "Main Campus" in cur_row[i]:
            adj_row = cur_row[:i + 1]
            index += i + 1
            print(len(adj_row))
            print(adj_row)
            #logic to handle row
            break
    else:
        print(cur_row)
        loop = 0


#print(extr[:13])
#print(adj_row)


# Row logic
# 0: Class code
# 1: Course subject
# 2: Section number, session, and class number (space separated)
# 3: Credit and Course Title
# 4: Class component
# 5: (USUALLY) time
# Followed by days, building/room, professor, enrollment, campus

# take len to know if its a little fucky
# kinda changes from page to page so 
# 10 means its working right
# 9 probably means no professor

# First 8 components always required
# inconsistent with/after meeting time