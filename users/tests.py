from django.test import TestCase

from classes.models import Class, Department, Section
from fcq.models import Professor
from users.forms import UserSignUpForm
from users.models import User

# Model unit test

# Create class for each test case, inherit Django's TestCase class


class UserTestCase(TestCase):
    # function that gets called first
    def setUp(self):
        new_user = User.objects.create(
            email="test@test.com",
            phone="1234567890",
            first_name="test",
            last_name="user",
            major="APPM",
        )

        test_department = Department.objects.create(name="Applied Math", code="APPM")
        # Class being made to add to schedule
        test_class = Class.objects.create(
            department=test_department, course_subject=1350, course_title="random math"
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

    # running a test case
    def testUserFields(self):
        """ User creation is succesfully saved and recalled """
        new_user = User.objects.get(first_name="test")
        self.assertEqual(new_user.email, "test@test.com")
        self.assertEqual(new_user.phone, "1234567890")
        self.assertEqual(new_user.first_name, "test")
        self.assertEqual(new_user.last_name, "user")
        self.assertEqual(new_user.major, "APPM")

    def testSignupForm(self):
        # Ensure blank form is not valid
        form = UserSignUpForm({})
        self.assertFalse(form.is_valid())

        # Errors on username, email, first_name, last_name, major, password, password2
        # NO error on phone
        self.assertEqual(len(form.errors), 7)
        self.assertEqual(form.errors.get("phone"), None)

        form = UserSignUpForm(
            {
                "username": "abc123",
                "email": "me@me.com",
                "phone": "1234567890",
                "first_name": "test",
                "last_name": "user",
                "major": "happy",
                "password1": "SuperSecretPassword123",
                "password2": "SuperSecretPassword123",
            }
        )

        # Invalid major
        self.assertEqual(len(form.errors), 1)

        form = UserSignUpForm(
            {
                "username": "abc123",
                "email": "me@me.com",
                "phone": "1234567890",
                "first_name": "test",
                "last_name": "user",
                "major": "APPM",
                "password1": "SuperSecretPassword123",
                "password2": "SuperSecretPassword123",
            }
        )

        print(form.errors)
        # Valid input
        self.assertTrue(form.is_valid())
