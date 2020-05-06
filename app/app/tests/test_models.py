from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """ method to test user creation with email and password """
        email = 'testmail@email.com'
        password = 'Testnew@11'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(email. user.email)
        self.assertTrue(user.check_password(password))
