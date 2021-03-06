import html
import operator
import re
from functools import reduce

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from classes.models import Class, Department, Section
from fcq.models import Professor

dept_dict = {
    "ACCT": "Accounting (ACCT)",
    "APRD": "Advertising, PR, Media Design (APRD)",
    "ASEN": "Aerospace Engineering (ASEN)",
    "AIRR": "Air Force Aerospace Studies (AIRR)",
    "ANTH": "Anthropology (ANTH)",
    "APPM": "Applied Math (APPM)",
    "ARAB": "Arabic (ARAB)",
    "AREN": "Architectural Engineering (AREN)",
    "ARCH": "Architecture (ARCH)",
    "ARTF": "Art Film Studies (ARTF)",
    "ARTH": "Art History (ARTH)",
    "ARTS": "Art Studio and Non-Studio (ARTS)",
    "ARSC": "Arts &amp; Sciences Courses (ARSC)",
    "ASIA": "Asian Studies (ASIA)",
    "ASTR": "Astrophysical &amp; Planetary Sci (ASTR)",
    "ATLS": "ATLAS (ATLS)",
    "ATOC": "Atmospheric &amp; Oceanic Sciences (ATOC)",
    "BAKR": "Baker Residential Acad Prgm (BAKR)",
    "BASE": "BCOR Applied Semester Exper (BASE)",
    "BCHM": "Biochemistry (BCHM)",
    "BMEN": "Biomedical Engineering (BMEN)",
    "BADM": "Business Administration (BADM)",
    "BCOR": "Business Core (BCOR)",
    "BPOL": "Business Environment &amp; Policy (BPOL)",
    "BSLW": "Business Law (BSLW)",
    "BUSM": "Business Minor (BUSM)",
    "CSVC": "Career Services (CSVC)",
    "CWCV": "Center for Western Civilizatio (CWCV)",
    "CAMW": "Center of the American West (CAMW)",
    "CEES": "Central &amp; East European Stdy (CEES)",
    "CHEN": "Chemical Engineering (CHEN)",
    "CHEM": "Chemistry (CHEM)",
    "CHIN": "Chinese (CHIN)",
    "CINE": "Cinema Stds/Moving Image Arts (CINE)",
    "CVEN": "Civil Engineering (CVEN)",
    "CWC": "Study of Western Civilization (CWC)",
    "GREK": "Classical Greek Language (GREK)",
    "CLAS": "Classics (CLAS)",
    "COEN": "Coll of Engineerng&amp;App Sci Adm (COEN)",
    "CMCI": "Coll of Media,Commncation,Info (CMCI)",
    "COMM": "Communication (COMM)",
    "COMR": "Communication Res Acad Prgm (COMR)",
    "COML": "Comparative Literature (COML)",
    "CSCI": "Computer Science (CSCI)",
    "CSPB": "Computer Science Post Bacc (CSPB)",
    "CNCR": "Concurrent Placeholder (CNCR)",
    "CMDP": "Critical Media Practices (CMDP)",
    "CESR": "Curr Emphasis in Soc Respnsbly (CESR)",
    "DNCE": "Dance (DNCE)",
    "DANE": "Danish (DANE)",
    "DHUM": "Digital Humanities (DHUM)",
    "EALC": "East Asian Langs &amp; Civilzatns (EALC)",
    "EBIO": "Ecology &amp; Evolutionary Biology (EBIO)",
    "ECON": "Economics (ECON)",
    "EDUC": "Education (EDUC)",
    "ECEN": "Electrical &amp; Computer Engr (ECEN)",
    "ENEN": "Energy Engineering (ENEN)",
    "EHON": "Engineering Honors (EHON)",
    "ENLP": "Engineering Leadership Program (ENLP)",
    "EMEN": "Engineering Management (EMEN)",
    "ENGL": "English (ENGL)",
    "ESLG": "English as a Second Language (ESLG)",
    "EDEN": "Engr for Developng Communities (EDEN)",
    "ESBM": "Entrepren &amp; Small Bus Mgmt (ESBM)",
    "ENST": "Environment and Sustainability (ENST)",
    "ENVD": "Environmental Design (ENVD)",
    "EVEN": "Environmental Engineering (EVEN)",
    "EPOD": "Environmental Prod of Design (EPOD)",
    "ENVS": "Environmental Studies (ENVS)",
    "ETHN": "Ethnic Studies (ETHN)",
    "TDXD": "Experience Design (TDXD)",
    "FARR": "Farrand Residential Acad Prgm (FARR)",
    "FRSI": "Farsi (FRSI)",
    "FILM": "Film Studies (FILM)",
    "FNCE": "Finance (FNCE)",
    "FINN": "Finnish (FINN)",
    "FYXP": "First Year Exploration (FYXP)",
    "FYSM": "First Year Seminar (FYSM)",
    "FREN": "French (FREN)",
    "GEEN": "General Engineering (GEEN)",
    "GEOG": "Geography (GEOG)",
    "GEOL": "Geological Sciences (GEOL)",
    "GRMN": "German (GRMN)",
    "GSAP": "Global Studies Residential Academic Program (GSAP)",
    "GSLL": "Germanic &amp; Slavic Lang &amp; Lit (GSLL)",
    "GRAD": "Graduate School (GRAD)",
    "GRTE": "Graduate Teacher Education (GRTE)",
    "HEBR": "Hebrew (HEBR)",
    "HIND": "Hindi/Urdu (HIND)",
    "HIST": "History (HIST)",
    "HONR": "Honors (HONR)",
    "HUMN": "Humanities (HUMN)",
    "HUEN": "Humanities for Engineers (HUEN)",
    "INDO": "Indonesian (INDO)",
    "BAIM": "Infm Mgmt/Business Analytics (BAIM)",
    "INFO": "Information Science (INFO)",
    "IPHY": "Integrative Physiology (IPHY)",
    "IMUS": "Intensive Music (IMUS)",
    "INST": "Interdisciplinary Studies (INST)",
    "IAFS": "International Affairs (IAFS)",
    "INBU": "International Business Cert (INBU)",
    "IAWP": "Intrmedia Art,Wrtg,Performance (IAWP)",
    "INVS": "INVST Community Studies (INVS)",
    "ITAL": "Italian (ITAL)",
    "JPNS": "Japanese (JPNS)",
    "JWST": "Jewish Studies (JWST)",
    "JRNL": "Journalism (JRNL)",
    "KREN": "Korean (KREN)",
    "LAND": "Landscape Architecture (LAND)",
    "LGTC": "Language Technology (LGTC)",
    "LAMS": "Latin American Studies (LAMS)",
    "LATN": "Latin Language (LATN)",
    "LAWS": "Law School (LAWS)",
    "LEAD": "Leadership Minor (LEAD)",
    "LDSP": "Leadership Res Acad Prgrm (LDSP)",
    "LGBT": "Lesbn/Gay/Bisexual Stdys (LGBT)",
    "LIBB": "Libby Residential Acad Prgm (LIBB)",
    "LIBR": "Libraries (LIBR)",
    "LING": "Linguistics (LING)",
    "MGMT": "Management (MGMT)",
    "MKTG": "Marketing (MKTG)",
    "ENVM": "Master of the Environment (ENVM)",
    "MSEN": "Materials Science&amp;Engineering (MSEN)",
    "MATH": "Mathematics (MATH)",
    "MBAX": "MBA Advanced Electives (MBAX)",
    "MBAC": "MBA Core (MBAC)",
    "MCEN": "Mechanical Engineering (MCEN)",
    "MDRP": "Media Research and Practice (MDRP)",
    "MDST": "Media Studies (MDST)",
    "MEMS": "Medieval &amp; Early Modern Stdys (MEMS)",
    "MILR": "Military Science (MILR)",
    "MCDB": "Molecular Cell &amp; Dev Biology (MCDB)",
    "MSBC": "MS Business Core (MSBC)",
    "MSBX": "MS Business Electives (MSBX)",
    "MUSM": "Museum (MUSM)",
    "MUSC": "Music (MUSC)",
    "MUEL": "Music Electives (MUEL)",
    "EMUS": "Music Ensemble (EMUS)",
    "NAVR": "Naval Science (NAVR)",
    "NRSC": "Neuroscience (NRSC)",
    "NCBE": "Non-credit Business Education (NCBE)",
    "NCEN": "Non-credit Engineering (NCEN)",
    "NCGR": "Non-credit German (NCGR)",
    "NCIE": "Non-credit Internat'l English (NCIE)",
    "NCTM": "Non-credit Technology &amp; Media (NCTM)",
    "NCTP": "Non-credit Test Preparation (NCTP)",
    "NRLN": "Norlin Scholars (NRLN)",
    "OPIM": "Operations &amp; Information MGMT (OPIM)",
    "ORMG": "Organization Management (ORMG)",
    "ORGN": "Organizational Behavior (ORGN)",
    "ORGL": "Organizational Leadership (ORGL)",
    "PACS": "Peace &amp; Conflict Studies (PACS)",
    "PMUS": "Performance Music (PMUS)",
    "PHIL": "Philosophy (PHIL)",
    "PHYS": "Physics (PHYS)",
    "PLAN": "Planning and Urban Design (PLAN)",
    "PSCI": "Political Science (PSCI)",
    "PORT": "Portuguese (PORT)",
    "PRLC": "Presidents Leadership Class (PRLC)",
    "PSYC": "Psychology (PSYC)",
    "REAL": "Real Estate (REAL)",
    "RCPR": "Reciprocal Exchange (RCPR)",
    "RLST": "Religious Studies (RLST)",
    "RSEI": "Renewable & Sustainable Energy Institute (RSEI)",
    "RUSS": "Russian (RUSS)",
    "SNSK": "Sanskrit (SNSK)",
    "SCAN": "Scandinavian (SCAN)",
    "SEWL": "Sewall Residential Acad Prgm (SEWL)",
    "SOCY": "Sociology (SOCY)",
    "SPAN": "Spanish (SPAN)",
    "SLHS": "Speech, Language &amp; Hearing Sci (SLHS)",
    "STAT": "Statistics (STAT)",
    "STDY": "Study Abroad (STDY)",
    "SUST": "Sustainability by Design RAP (SUST)",
    "SSIR": "Sustainablty&amp;Soc Innovtn RAP (SSIR)",
    "SWED": "Swedish (SWED)",
    "CYBR": "Technology, Cybersec &amp; Policy (CYBR)",
    "TLEN": "Telecommunications (TLEN)",
    "THDN": "Theater &amp; Dance (THDN)",
    "THTR": "Theatre (THTR)",
    "TMUS": "Thesis Music (TMUS)",
    "WGST": "Women and Gender Studies (WGST)",
    "WRTG": "Writing and Rhetoric (WRTG)",
}

known_differences = {
    "CHE": "CHEM",
    "CAM": "CAMW",
    "GRE": "GREK",
    "DNC": "DNCE",
    "ECO": "ECON",
    "GEO": "GEOG",
    "GRM": "GRMN",
    "HUM": "HUMN",
    "MCD": "MCDB",
    "MUS": "MUSM",
    "NRS": "NRSC",
    "SWE": "SWED",
    "WRT": "WRTG",
    "EHO": "EHON",
    "EME": "EMEN",
    "HUE": "HUEN",
    "MCE": "MCEN",
    "COM": "COMM",
    "CMD": "CMDP",
    "EMU": "EMUS",
    "PMU": "PMUS",
    "BAD": "BADM",
    "BCO": "BCOR",
    "BSL": "BSLW",
    "MGM": "MGMT",
    "MKT": "MKTG",
    "MBA": "MBAC",
    "ORM": "ORMG",
    "ARC": "ARCH",
    "EDU": "EDUC",
    "LAW": "LAWS",
    "WMST": "WGST",
    "JOUR": "JRNL",
}


def PopulateClasses():
    # Class.objects.all().delete() # we won't need this after changes
    f = open("classes/management/commands/class_schedule.csv", "r")

    failures = 0
    adds = 0

    for line in f:
        course = Section()
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[: len(line) - 1].split(",")]
        # deal with known differences below:
        adjust_code = known_differences.get(data[0])
        if adjust_code:
            data[0] = adjust_code
        ############################
        # create new department/class object here, and link it to the section
        try:
            name = html.unescape(
                dept_dict[data[0]]
            )  # some characters like '&' are encoded as 'amp;'
            department = Department.objects.filter(name=name).first()
            if not department:
                department = Department(name=name, code=data[0])
                department.save()

            # match class if these params match. Omit course title in case of
            # slight inconsitancies (such as trailing spaces)
            class_obj = Class.objects.filter(
                department=department, course_subject=data[1]
            ).first()
            if not class_obj:
                class_obj = Class(
                    department=department, course_subject=data[1], course_title=data[6]
                )
                class_obj.save()
        except KeyError:
            failures += 1
            continue
        ############################
        # get instructor object, set to none if not found
        name_q = re.split("\W", data[12])
        professor = Professor.objects.filter(
            reduce(
                operator.and_,
                (
                    (Q(firstName__icontains=x) | Q(lastName__icontains=x))
                    for x in name_q
                ),
            )
        ).first()
        if not professor or name_q == ['']:
            professor = None
        section_obj = Section.objects.filter(
            parent_class=class_obj,
            section_number=data[2],
            session=data[3],
            class_number=data[4],
            credit=data[5],
            class_component=data[7],
            start_time=data[8],
            end_time=data[9],
            days=data[10],
            building_room=data[11],
            professor=professor,
            max_enrollment=data[13],
            campus=data[14],
        ).first()

        if not section_obj:
            course.parent_class = class_obj
            course.section_number = data[2]
            course.session = data[3]
            course.class_number = data[4]
            course.credit = data[5]
            course.class_component = data[7]
            course.start_time = data[8]
            course.end_time = data[9]
            course.days = data[10]
            course.building_room = data[11]
            course.professor = professor
            course.max_enrollment = data[13]
            course.campus = data[14]
            try:
                with transaction.atomic():
                    course.save()
                    adds += 1
            except:
                print(data)
                failures += 1
    print("Added {} classes with {} failures".format(adds, failures))
    f.close()  # close file
    if failures == 0:
        return True  # for testing
    else:
        return False


class Command(BaseCommand):
    print(
        "Updating classes with class_schedule.csv found in classes/management/commands"
    )
    # print("This will take ~30 seconds")

    def handle(self, *args, **kwargs):
        # Return values are for tests. test kwarg flag will be set if used with test
        in_test = kwargs.pop("test", False)
        if in_test:
            if PopulateClasses():
                return True
            else:
                return False
        else:
            PopulateClasses()
