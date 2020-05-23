from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def sample_user(email='john7ric@mail.com', password='open@123'):
    """
    create a basic sample user
    """
    return get_user_model().objects.create_user(email, password)

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
        email = 'yamaha@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email, password='Open@12')

        self.assertEqual(user.email, email.lower())

    def test_create_use_with_invalid_email(self):
        """ test if user cant be created with incalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password='open@123')

    def test_create_superuser(self):
        """ test if create super user is crateng users with is_staff
         and is_superuser set to true"""
        user = get_user_model().objects.create_superuser(
             'mail@domain.com',
             'password@123'
         )

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_tag_str(self):
        """
        test the string representation of created model
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingrediant_model_str(self):
        """
        test the ingrediant intance can be created
        """
        ingrediant = models.Ingrediant.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingrediant), ingrediant.name)
