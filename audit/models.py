from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from classes.models import Class
from django.db import transaction


class AuditCreator:

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

    def createCSAudit(CSAudit):
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

        # CSAudit.userId = userId
        # I don't think I need to wrap this in a try block
        # with transaction.atomic():
        #    CSAudit.save()

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
            data = [x.replace(";", ",")
                    for x in line[:len(line) - 1].split(",")]
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

        return audit

# webscrape humanities classes off classes.colorado.edu?
# I have natsci classes already


class Audit(models.Model):

    # Database
    # Each audit is made of many DegreeSection objects, does not individually hold data

    # Relation
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Audit, self).save(*args, **kwargs)
            # new object
            self.createCSAudit()

        super(Audit, self).save(*args, **kwargs)

    # Helper methods
    def loadSection(self, filename, Section):
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

    def createCSAudit(self):
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

        # load and save all sections
        OverallSection.auditId = self
        MajorSection.auditId = self
        NatSciSection.auditId = self
        AllHumn.auditId = self
        UpperHumn.auditId = self

        with transaction.atomic():
            OverallSection.save()
            MajorSection.save()
            NatSciSection.save()
            AllHumn.save()
            UpperHumn.save()

        NatSciSection = self.loadSection(
            "audit/management/commands/natsci.csv", NatSciSection)

        file = open('audit/management/commands/csAudit.csv', 'r')
        failures = 0
        for line in file:
            prereq = Prerequisite()
            data = [x.replace(";", ",")
                    for x in line[:len(line) - 1].split(",")]
            prereq.requiredNumber = data[0]
            prereq.possibleClasses = data[1:]
            prereq.auditId = self

            try:
                with transaction.atomic():
                    prereq.save()
            except:
                failures += 1
        file.close()
        print("Failed", failures, "prereqs")


# DegreeSection holds requirements for a section of the degree (i.e. nat sci, humanities, etc)
class DegreeSection(models.Model):

    # Database
    sectionName = models.CharField(max_length=40)
    creditRequirement = models.IntegerField()
    currentCredit = models.IntegerField()
    # Relation
    appliedClasses = models.ManyToManyField(
        Class, related_name="appliedClasses")
    auditId = models.ForeignKey(Audit, on_delete=models.CASCADE)


# Model to define the classes a user has completed. A new object created for each class a user has completed
class CompletedClass(models.Model):

    # Database
    completedClass = models.CharField(max_length=10)
    # Relation
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


# Model to define the prerequisites for taking a class. ArrayField allows for multiple possible prereqs
# RequiredNumber allows defining how many need to be taken (i.e. take 6 of the following)
class Prerequisite(models.Model):

    # Database
    requiredNumber = models.IntegerField()
    possibleClasses = ArrayField(models.CharField(max_length=10),)
    # Relation. Each prereq has a class or audit exclusive
    # classId = models.ForeignKey(
    #    Class, on_delete=models.CASCADE, blank=True, null=True)
    # I believe this is many-to-many, as there are many CSCI1300 and many CSCI2270, any 1300 is a prereq for any 2270
    classes = models.ManyToManyField(Class, related_name="classes")
    auditId = models.ForeignKey(
        Audit, on_delete=models.CASCADE, blank=True, null=True)
