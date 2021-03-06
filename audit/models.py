from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from classes.models import Class, Department
from django.db import transaction


class AuditFactory:

    def loadSection(self, audit, filename):
        Section = DegreeSection()
        file = open(filename, "r")
        line = file.readline().split(",")
        Section.sectionName = line[0]
        Section.creditRequirement = line[1]
        Section.currentCredit = 0
        Section.audit = audit

        with transaction.atomic():
            Section.save()

        for className in line[2:]:
            classDepartment = className[0:-4]
            courseSubject = className[-4:]
            objects = Class.objects.filter(department__code=classDepartment).filter(
                course_subject=courseSubject)
            for obj in objects:
                Section.appliedClasses.add(obj)
        file.close()
        return Section

    def createAudit(self, audit, name):
        OverallSection = self.loadSection(audit,
                                          "audit/requirements/{}/overall.csv".format(name))
        MajorSection = self.loadSection(audit,
                                        "audit/requirements/{}/major.csv".format(name))
        NatSciSection = self.loadSection(audit,
                                         "audit/requirements/{}/natsci.csv".format(name))
        AllHumn = self.loadSection(audit,
                                   "audit/requirements/{}/humanities.csv".format(name))
        UpperHumn = self.loadSection(audit,
                                     "audit/requirements/{}/upperhumanities.csv".format(name))

        file = open('audit/requirements/{}/required.csv'.format(name), 'r')
        failures = 0
        prereqFailures = []

        for line in file:
            prereq = Prerequisite()
            data = [x.replace(";", ",")
                    for x in line[:len(line) - 1].split(",")]
            prereq.requiredNumber = data[0]
            prereq.corequisite = data[1]
            prereq.audit = audit

            try:
                with transaction.atomic():
                    prereq.save()
            except:
                failures += 1

            for name in data[2:]:
                departCode = name[:4]
                classNumber = name[4:]
                try:
                    prereq.possibleClasses.add(Class.objects.filter(
                        course_subject=classNumber).filter(department__code=departCode).get())
                except:
                    prereqFailures += [name]
        file.close()
        if failures > 0:
            print("Failed", failures, "prereqs")
            print("Failed to add classes:\n", prereqFailures)
        return audit


# webscrape humanities classes off classes.colorado.edu?
# I have natsci classes already
class Audit(models.Model):

    # Database
    # Each audit is made of many DegreeSection objects, does not individually hold data

    # Relation
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    factory = AuditFactory()

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Audit, self).save(*args, **kwargs)
            # would need a smarter way if we're doing more than one major
            if self.user.major == "CSCI":
                self = self.factory.createAudit(self, "bscs")

        super(Audit, self).save(*args, **kwargs)


# DegreeSection holds requirements for a section of the degree (i.e. nat sci, humanities, etc)
class DegreeSection(models.Model):

    # Database
    sectionName = models.CharField(max_length=40)
    creditRequirement = models.IntegerField()
    currentCredit = models.IntegerField()
    # Relation
    appliedClasses = models.ManyToManyField(
        Class, related_name="appliedClasses")
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)


# Model to define the prerequisites for taking a class. ArrayField allows for multiple possible prereqs
# RequiredNumber allows defining how many need to be taken (i.e. take 6 of the following)
class Prerequisite(models.Model):

    # Database
    requiredNumber = models.IntegerField()
    corequisite = models.BooleanField()
    #possibleClasses = ArrayField(models.CharField(max_length=10),)
    # Relation. Each prereq has a class or audit exclusive
    classes = models.ForeignKey(
        Class, on_delete=models.CASCADE, blank=True, null=True)
    audit = models.ForeignKey(
        Audit, on_delete=models.CASCADE, blank=True, null=True)
    possibleClasses = models.ManyToManyField(
        Class, related_name="possibleClasses")
