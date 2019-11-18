from django.core.management.base import BaseCommand, CommandError
from audit.models import Audit, Prerequisite
from django.db import transaction
from users.models import User


def createCSAudit(userId):
    CSAudit = Audit()
    CSAudit.creditRequirement = 128
    CSAudit.majorRequirement = 58
    CSAudit.currentCredit = 0
    CSAudit.currentMajorCredit = 0
    CSAudit.currentCredit = 0
    CSAudit.userId = userId
    # I don't think I need to wrap this in a try block
    with transaction.atomic():
        CSAudit.save()

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
    print("Failed", failures, "prereqs")


class Command(BaseCommand):
    print("Adding new audit for BS CS with csAudit.csv")

    def handle(self, *args, **options):
        # temp do for user 7 (me)
        user = User.objects.get(pk=7)
        createCSAudit(user)
