from django.test import TestCase
from users.models import User

# Model unit test

# Create class for each test case, inherit Django's TestCase class
class UserTestCase(TestCase):
    # function that gets called first
    def setUp(self):
        new_user = User.objects.create(email="test@test.com", phone="1234567890", first_name="test", last_name="user", major="APPM")

    # running a test case
    def testUserFields(self):
        """ User creation is succesfully saved and recalled """
        new_user = User.objects.get(first_name="test")
        self.assertEqual(new_user.email, "test@test.com")
        self.assertEqual(new_user.phone, "1234567890")
        self.assertEqual(new_user.first_name, "test")
        self.assertEqual(new_user.last_name, "user")
        self.assertEqual(new_user.major, "APPM")

