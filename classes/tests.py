from django.test import TestCase
from classes.management.commands.updateclasses import Command

# Create your tests here.


class ClassTestCase(TestCase):
    # function that gets called first
    def setUp(self):
        pass

    def testClassImport(self):
        # this command (updateclasses) will return false if any failures occur
        self.assertTrue(
            Command.handle(Command, test=True)
        )  # call with test option (kwarg)
