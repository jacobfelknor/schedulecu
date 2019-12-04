from django.contrib.auth import login
from django.test import Client, TestCase

from classes.models import Class, Department, Section
from fcq.models import Professor
from users.forms import UserSignUpForm
from users.models import User

# Model unit test

# Create class for each test case, inherit Django's TestCase class


class ScheduleTestCase(TestCase):
    section_id = None
    section_obj = None
    # function that gets called first

    def setUp(self):
        """ Set up new user using UserSignUp Form to test schedule. Uses similar method as in the user test
            Tests whether or not the user's schedule is assigned correctly on creation
        """
        test_department = Department.objects.create(
            name="Computer Science (CSCI)", code="CSCI"
        )
        # Class being made to add to schedule
        test_class = Class.objects.create(
            department=test_department, course_subject=1350, course_title="random cs"
        )
        test_professor = Professor.objects.create(firstName="Billy", lastName="Joe")
        test_section = Section.objects.create(
            parent_class=test_class,
            section_number="100",
            session="B",
            class_number="12345",
            credit="4",
            class_component="LEC",
            start_time="10:00 AM",
            end_time="10:50 AM",
            days="MWF",
            building_room="MATH100",
            professor=test_professor,
            max_enrollment=200,
            campus="Main Campus",
        )
        # Save this section's id/obj for later use
        self.section_id = test_section.id
        self.section_obj = test_section

        # Save class id/obj for later use
        self.class_id = test_class.id
        self.class_obj = test_class

        # Ensure blank form is not valid
        form = UserSignUpForm({})
        self.assertFalse(form.is_valid())

        # Errors on username, email, first_name, last_name, major, password, password2
        # NO error on phone
        self.assertEqual(len(form.errors), 7)
        self.assertEqual(form.errors.get("phone"), None)

        form = UserSignUpForm(
            {
                "username": "testing123",
                "email": "test@test.com",
                "phone": "1234567890",
                "first_name": "Test",
                "last_name": "User",
                "major": "CSCI",
                "password1": "SuperSecretPassword123",
                "password2": "SuperSecretPassword123",
            }
        )
        # Valid input
        self.assertTrue(form.is_valid())
        form.save()

    def testScheduleAssignment(self):
        user = User.objects.get(username="testing123")
        self.assertIsNotNone(user.schedule)

    def testAddClassToSchedule(self):
        user = User.objects.get(username="testing123")
        self.assertIsNotNone(user)
        self.assertEqual(
            len(user.schedule.classes.all()), 0
        )  # make sure schedule exists, but empty
        c = Client()
        logged_in = c.login(
            username="testing123", password="SuperSecretPassword123"
        )  # login user
        c.get(
            "/schedules/add_to_schedule/",
            {"section_id": self.section_id,
             "class_id": self.class_id}
        )  # make request to view to add class to schedule
        self.assertEqual(len(user.schedule.classes.all()),
                         1)  # confirm class was added

        self.assertEqual(
            user.schedule.classes.first(), self.section_obj
        )  # confirm class was added correctly
