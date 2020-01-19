import os
import html
import numpy as np
from django.db import transaction
from classes.models import Class, Department
from useraudits.models import UserAuditEntry, UserAuditTransferEntry, UserAuditInfo


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


def getInfo(user):
    weights = {
        'A' : 4.0,
        'A-' : 3.7,
        'B+' : 3.3,
        'B' : 3.0,
        'B-' : 2.7,
        'C+' : 2.3,
        'C' : 2.0,
        'C-' : 1.7,
        'D+' : 1.3,
        'D' : 1.0,
        'D-' : 0.7,
        'F' : 0.0,
    }

    userAudits = UserAuditEntry.objects.filter(user=user)
    userTransfers = UserAuditTransferEntry.objects.filter(user=user)
    
    gpa_cu = 0.0
    gpa_transfer = 0.0
    gpa_complete = 0.0
    progress = 0.0
    attempted = 0.0
    earned = 0.0
    num_cu_courses = 0
    num_transfers = 0

    cu_points = 0.0
    cu_credits = 0.0
    transfer_points = 0.0
    transfer_credits = 0.0

    for entry in userAudits:
        if entry.transfer == True:
            num_transfers += 1
            transfer_credits += entry.credits
            transfer_points += entry.credits * weights[entry.grade]
        else:
            num_cu_courses += 1
            if entry.grade == '*':
                progress += entry.credits
            else:
                cu_credits += entry.credits
                cu_points += entry.credits * weights[entry.grade]

    for entry in userTransfers:
        num_transfers += 1
        transfer_credits += entry.credits
        transfer_points += entry.credits * weights[entry.grade]

    if cu_credits > 0:
        gpa_cu = round(cu_points / cu_credits,2)
    if transfer_credits > 0:
        gpa_transfer = round(transfer_points / transfer_credits,2)
    earned = cu_credits + transfer_credits
    if earned > 0:
        gpa_complete = round((cu_points + transfer_points) / earned,2)
    attempted = cu_credits

    return [gpa_cu,gpa_transfer,gpa_complete,progress,attempted,earned,transfer_credits,num_cu_courses,num_transfers]


def addUserInfo(user):
    auditInfo = getInfo(user)
    userObject = UserAuditInfo()
    userObject.user = user
    userObject.gpa_cu = auditInfo[0]
    userObject.gpa_transfer = auditInfo[1]
    userObject.gpa_complete = auditInfo[2]
    userObject.progress = auditInfo[3]
    userObject.attempted = auditInfo[4]
    userObject.earned = auditInfo[5]
    userObject.transfer_credits = auditInfo[6]
    userObject.num_cu_courses = auditInfo[7]
    userObject.num_transfers = auditInfo[8]
    userObject.save()
    

def addEntries(audit, auditTransfers, user):
    entryAdds = 0
    entryFails = 0
    for data in audit:
        # print(data)
        entry = UserAuditEntry()
        entry.user = user
        adjust_code = known_differences.get(data[2])
        if adjust_code:
            data[2] = adjust_code
        if dept_dict[data[2]]:
            name = html.unescape(dept_dict[data[2]])
        else:
            name = data[2]
        department = Department.objects.filter(name=name).first()
        subject = int(data[3])
        course_obj = Class.objects.filter(department=department, course_subject=subject).first()
        if not course_obj:
            course_obj = Class(department=department, course_subject=subject, course_title='**Course Title Unavailable**')
            course_obj.save()
        entry.course = course_obj
        entry.year = '20' + data[1]
        entry.semester = data[0]
        entry.grade = data[4]
        entry.credits = data[5]
        entry.transfer = data[6]
        try:
            with transaction.atomic():
                    entry.save()
                    entryAdds += 1
        except DatabaseError:
            print(data)
            entryFails += 1
            continue
    print(entryAdds, "entries added;", entryFails, "entries failed")

    transferAdds = 0
    transferFails = 0
    for data in auditTransfers:
        entry = UserAuditTransferEntry()
        entry.user = user
        adjust_code = known_differences.get(data[2])
        if adjust_code:
            data[2] = adjust_code
        if dept_dict[data[2]]:
            name = html.unescape(dept_dict[data[2]])
        else:
            name = data[2]
        department = Department.objects.filter(name=name).first()

        entry.department = department
        entry.level = data[3]
        entry.year = '20' + data[1]
        entry.semester = data[0]
        entry.grade = data[4]
        entry.credits = data[5]

        try:
            with transaction.atomic():
                    entry.save()
                    transferAdds += 1
        except DatabaseError:
            print(data)
            transferFails += 1
            continue
    print(transferAdds, "transfers added;", transferFails, "transfers failed")


def removeEntries(user):
    userInfo = UserAuditInfo.objects.filter(user=user)
    if userInfo:
        userInfo.delete()
        print("user deleted")

    userAudits = UserAuditEntry.objects.filter(user=user)
    userTransfers = UserAuditTransferEntry.objects.filter(user=user)
    count = 0
    if userAudits:
        for entry in userAudits:
            entry.delete()
            count += 1
    if userTransfers:
        for entry in userTransfers:
            entry.delete()
            count += 1
    print(count, "entries deleted")

