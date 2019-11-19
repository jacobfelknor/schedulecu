from django.core.management.base import BaseCommand, CommandError
from audit.models import Audit, Prerequisite, DegreeSection
from classes.models import Class
from django.db import transaction
from users.models import User


def loadSection(filename, Section):
    file = open(filename, "r")
    line = file.readline()
    Section.creditRequirement = line.split(",")[0]
    for className in line.split(",")[1:]:
        classDepartment = className[0:-4]
        courseSubject = className[-4:]
        objects = Class.objects.filter(department=classDepartment).filter(
            course_subject=courseSubject)
        for obj in objects:
            Section.appliedClasses.add(obj)
    file.close()
    return Section


def createCSAudit(userId):
    CSAudit = Audit()
    OverallSection = DegreeSection()
    MajorSection = DegreeSection()
    NatSciSection = DegreeSection()
    AllHumn = DegreeSection()
    UpperHumn = DegreeSection()
    OverallSection.sectionName = "Overall"
    MajorSection.sectionName = "Major"
    NatSciSection.sectionName = "Natural Science"
    AllHumn.sectionName = "Humanities"
    UpperHumn.sectionName = "Upper Humanities"
    OverallSection.creditRequirement = 128
    OverallSection.currentCredit = 0
    MajorSection.creditRequirement = 58
    MajorSection.currentCredit = 0
    NatSciSection.creditRequirement = 17
    NatSciSection.currentCredit = 0
    AllHumn.creditRequirement = 15
    AllHumn.currentCredit = 0
    UpperHumn.creditRequirement = 6
    UpperHumn.currentCredit = 0

    CSAudit.userId = userId
    # I don't think I need to wrap this in a try block
    with transaction.atomic():
        CSAudit.save()

    # load and save all sections
    OverallSection.auditId = CSAudit
    MajorSection.auditId = CSAudit
    NatSciSection.auditId = CSAudit
    AllHumn.auditId = CSAudit
    UpperHumn.auditId = CSAudit

    with transaction.atomic():
        OverallSection.save()
        MajorSection.save()
        NatSciSection.save()
        AllHumn.save()
        UpperHumn.save()

    NatSciSection = loadSection(
        "audit/management/commands/natsci.csv", NatSciSection)

    file = open('audit/management/commands/csAudit.csv', 'r')
    failures = 0
    for line in file:
        prereq = Prerequisite()
        data = [x.replace(";", ",") for x in line[:len(line) - 1].split(",")]
        prereq.requiredNumber = data[0]
        prereq.possibleClasses = data[1:]
        prereq.auditId = CSAudit

        try:
            with transaction.atomic():
                prereq.save()
        except:
            failures += 1
    file.close()
    print("Failed", failures, "prereqs")


class Command(BaseCommand):
    print("Adding new audit for BS CS with csAudit.csv")

    def handle(self, *args, **options):
        # temp do for user 7 (me)
        user = User.objects.get(pk=7)
        createCSAudit(user)
