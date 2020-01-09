from django.core.management.base import BaseCommand, CommandError
from fcq.management.commands import populateFCQ, populateProfs
from classes.management.commands import updateclasses
from audit.management.commands import addprereqs


class Command(BaseCommand):
    print("Initializing Database\nThis will take a while ~10-15min")

    def handle(self, *args, **kwargs):
        """ initialize database using the commands in the correct order """
        populateProfs.Command.handle(populateProfs.Command)
        updateclasses.Command.handle(updateclasses.Command)
        populateFCQ.Command.handle(populateFCQ.Command)
        addprereqs.Command.handle(addprereqs.Command)
