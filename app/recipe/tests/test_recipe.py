from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """
    Create a sample user with defaults for helpoing tests
    """
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)
    defaults['user'] = user

    return Recipe.objects.create(**defaults)


class PublicRecipeAPITests(TestCase):
    """"
    Testing for unauthorized acces for  Recipe API Components
    """

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_recipe_access_fails(self):
        """
        test for unauthorized access failure on recipe api
        """
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """
    Test Suite for authorized user Recipe API Compnents
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@mail.com',
            name='Test User',
            password='Open@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_recipe_created(self):
        """
        Test if the recipes created are retreived successfully
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_user_recipes_only(self):
        """
        Test only the recipes for corresponding user is listed
        """
        user2 = get_user_model().objects.create_user(
            email='mail.kkk@.com',
            password='39393sdnkds',
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
