from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """ helper function to create users for tests """
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """ Test for user api (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ test user creation with valid payload"""
        payload = {
            'name': 'Ashwati Nair',
            'email': 'ashwati.nair@ibsplc.com',
            'password': 'abc@1234'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_existing_user(self):
        """ test creating already exiting user returns error """
        payload = {
            'email': 'john7ric@mail.com',
            'name': 'Test Name',
            'password': '123456'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ test if request fails if password is less than 5 chars """
        payload = {'email': 'ashwati@mail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ test if token is created for user"""
        payload = {
            'email': 'user@Email.com',
            'password': 'test@123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """ test no a token is created created for invalid user credentials"""
        create_user(email='johnwick@gmail.com', password= 'Open@123')
        payload = {
            'email': 'johnwick@gmail.com',
            'password': 'Open@1343'
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('password', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_no_user(self):
        """ test to check if no authtocken is issued for non 
        existing user"""
        payload = {
            'email': 'mail@test.com',
            'password': 'TEST@1234'
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('password', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_fields(self):
        """ test if token is not issued with missing fields """
        res = self.client.post(TOKEN_URL, {'email': 'mail', 'password': 'lulz'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
