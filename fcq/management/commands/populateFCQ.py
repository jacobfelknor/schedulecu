import os
import html

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from fcq.models import Professor, FCQ, Department, Class


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


def PopulateFCQ():
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, 'clean_fcq.csv')
    f = open(filename, 'r')
    failures = 0
    fcqAdds = 0
    depAdds = 0
    profAdds = 0
    courseAdds = 0
    for line in f:
        # remove newline char at end and replace temporary semicolons back to commas
        data = [x.replace(";", ",") for x in line[: len(line) - 1].split(",")]
        # deal with known differences below:
        adjust_code = known_differences.get(data[5])
        if adjust_code:
            data[5] = adjust_code
        # create new department/class object here, and link it to the section
        try:
            prof = data[9].split(',')
            first = prof[1][1:]
            last = prof[0]
            professor1 = Professor.objects.filter(
                lastName=last,
                firstName=first,
            ).first()
            #if professor does not exist, add them
            if not professor1:
                professor1 = Professor(lastName=last,firstName=first)
                professor1.save()
                profAdds += 1

            department = Department.objects.filter(name=data[5]).first()
            if not department:
                department = Department(name=data[5], code=data[5])
                department.save()
                depAdds += 1

            # match class if these params match. Omit course title in case of
            # slight inconsitancies (such as trailing spaces)
            course1 = Class.objects.filter(
                department=department, course_subject=data[6]
            ).first()
            if not course1:
                course1 = Class(
                    department=department, course_subject=data[6], course_title=data[8]
                )
                course1.save()
                courseAdds += 1
        except KeyError:
            failures += 1
            print(data[5],data[6])
            continue
        fcq = FCQ.objects.filter(
            year=data[1],
            semester=data[0],
            section=data[7],
            courseType=data[11],
            online=data[13],
            size=data[14],
            numResponses=data[15],
            challenge=data[19],
            learned=data[20],
            courseRating=data[21],
            profEffect=data[22],
            profRating=data[25],
            courseSD=data[26],
            profSD=data[27],
            professor=professor1,
            course=course1
        ).first()
        if not fcq:
            fcq = FCQ()
            fcq.year = data[1]
            fcq.semester = data[0]
            fcq.section = data[7]
            fcq.courseType = data[11]
            fcq.online = data[13]
            fcq.size = data[14]
            fcq.numResponses = data[15]
            fcq.challenge = data[19]
            fcq.learned = data[20]
            fcq.courseRating = data[21]
            fcq.profEffect = data[22]
            fcq.profRating = data[25]
            fcq.courseSD = data[26]
            fcq.profSD = data[27]
            fcq.professor = professor1
            fcq.course = course1
            try:
                with transaction.atomic():
                    fcq.save()
                    fcqAdds += 1
            except:
                print(data)
                failures += 1
    print("Added {} departments, {} professors, {} courses, and {} FCQ's with {} failures".format(depAdds, profAdds, courseAdds, fcqAdds, failures))
    f.close()  # close file
    if failures == 0:
        return True  # for testing
    else:
        return False

class Command(BaseCommand):
    print("Filling FCQ and Professor database tables...")
    def handle(self, *args, **kwargs):
        # Return values are for tests. test kwarg flag will be set if used with test
        in_test = kwargs.pop("test", False)
        if in_test:
            if PopulateFCQ():
                return True
            else:
                return False
        else:
            PopulateFCQ()
            # Professor.objects.all().delete()
            # FCQ.objects.all().delete()
