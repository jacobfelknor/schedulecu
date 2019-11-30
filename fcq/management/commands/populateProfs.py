import os

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from fcq.models import Professor


class Command(BaseCommand):
    def handle(self, *args, **options):
        directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(directory, "clean_fcq.csv")
        f = open(filename, "r")
        failures = 0
        profAdds = 0
        for line in f:
            # remove newline char at end and replace temporary semicolons back to commas
            data = [x.replace(";", ",") for x in line[: len(line) - 1].split(",")]
            try:
                prof = data[9].split(",")
                first = prof[1][1:]
                last = prof[0]
                prof_obj = Professor.objects.filter(
                    lastName=last, firstName=first
                ).first()
                # if professor does not exist, add them
                if not prof_obj:
                    prof_obj = Professor(lastName=last, firstName=first)
                    prof_obj.save()
                    profAdds += 1
            except DatabaseError:
                failures += 1
                continue
