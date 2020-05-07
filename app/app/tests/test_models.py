from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """ method to test user creation with email and password """
        email = 'testmail@email.com'
        password = 'Testnew@11'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_normalized_succesfully(self):
        """test if user is created with normalized email"""
        email = 'john7ric@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email, password='Open@12')

        self.assertEqual(user.email, email.lower())

    def test_create_use_with_invalid_email(self):
        """ tet if user cant be created with incalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password='open@123')
