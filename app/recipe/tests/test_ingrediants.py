from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingrediant
from recipe.serializers import IngrediantSerializer

INGREDIANTS_URL = reverse('recipe:ingrediant-list')


class PublicIngrediantsAPITests(TestCase):
    """
    Tests for publicaly available Ingrediants API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required_for_ingrediants(self):
        """
        Test user is authorized to retreive ingrediants
        """
        res = self.client.post(INGREDIANTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrediantsAPITests(TestCase):
    """
    Tests the ingrediants api whcih needs authorization
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'john7ric@mail.com',
            'open@949404'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_ingrediants(self):
        """
        test if the ingrediants created are listed correctly
        """
        Ingrediant.objects.create(
            user=self.user,
            name='Vinegar'
        )
        Ingrediant.objects.create(
            user=self.user,
            name='Mango'
        )
        ingrediants = Ingrediant.objects.all().order_by('-name')
        data = IngrediantSerializer(ingrediants, many=True).data

        res = self.client.get(INGREDIANTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)

    def test_list_users_ingrediants(self):
        """
        Test only ingrediants of a user are listed
        """
        user2 = get_user_model().objects.create_user(
            'user@mail.com',
            'open@19939393'
        )
        Ingrediant.objects.create(
            user=user2,
            name='Vinegar'
        )
        ingrediant = Ingrediant.objects.create(
            user=self.user,
            name='Kale'
        )

        res = self.client.get(INGREDIANTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingrediant.name)

    def test_create_valid_ingrediant(self):
        """
        Test for creatign a valid ingrediant
        """
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIANTS_URL, payload)

        exists = Ingrediant.objects.filter(
            name=payload['name']
        ).exists

        self.assertTrue(exists)

    def test_invalid_ingrediant_creation(self):
        """
        Test if invalid ingrediant creation is failed with bad request
        """
        res = self.client.post(INGREDIANTS_URL, {'name': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
