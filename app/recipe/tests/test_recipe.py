from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingrediant
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

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


def detail_url(recipe_id):
    """
    Detail url for a recipe
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main Course'):
    """
    Sample tag for aiding recipe tests
    """
    return Tag.objects.create(user=user, name=name)


def sample_ingrediant(user, name='Cinnamon'):
    """
    Sample ingrediant for recipe tests
    """
    return Ingrediant.objects.create(user=user, name=name)


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

    def test_recipe_detail(self):
        """
        Tests for detail of a recipe
        """
        recipe = sample_recipe(user=self.user)

        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingrediants.add(sample_ingrediant(user=self.user))
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """
        Tewst for creating a basic recipe
        """
        payload = {
            'title': 'Mushroom Masala',
            'time_minutes': 20,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """
        test for creating recipe with tags
        """
        tag1 = sample_tag(user=self.user, name='Dessert')
        tag2 = sample_tag(user=self.user, name='Ice Cream')
        payload = {
            'title': 'Butterscotch Choconut',
            'time_minutes': 15,
            'price': 5.00,
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()

        self.assertEqual(len(tags), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingrediants(self):
        """
        Test for creating recipe with ingrediants
        """
        ingrediant1 = sample_ingrediant(user=self.user, name='Nuts')
        ingrediant2 = sample_ingrediant(user=self.user, name='Ice cream')
        payload = {
            'title': 'Butterscotch Choconut',
            'time_minutes': 5,
            'price': 5.00,
            'ingrediants': [ingrediant1.id, ingrediant2.id]
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        ingrediants = recipe.ingrediants.all()
        self.assertEqual(len(ingrediants), 2)
        self.assertIn(ingrediant1, ingrediants)
        self.assertIn(ingrediant2, ingrediants)

    def test_recipe_partial_update(self):
        """
        test for partial update for recipe object
        """

        recipe = sample_recipe(user=self.user)
        tag1 = sample_tag(user=self.user, name='Dessert')
        tag2 = sample_tag(user=self.user, name='Cake')
        payload = {
            'title': 'Butter Cake',
            'time_minutes': 15,
            'price': 15.00
        }
        recipe.tags.add(tag1)
        recipe.tags.add(tag2)

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], recipe.title)
        self.assertEqual(payload['time_minutes'], recipe.time_minutes)
        self.assertEqual(payload['price'], recipe.price)
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_update_recipe_put(self):
        """
        Test put requests on recipe objects
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user, name='Main Course'))
        recipe.tags.add(sample_tag(user=self.user, name='Chicken Dish'))

        payload = {
            'title': 'Chicken Tikka',
            'time_minutes': 20,
            'price': 5.00,
            'link': 'www.linkedin.in/john7ric',
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        recipe.refresh_from_db()
        tags = recipe.tags.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], recipe.title)
        self.assertEqual(payload['time_minutes'], recipe.time_minutes)
        self.assertEqual(payload['price'], recipe.price)
        self.assertEqual(payload['link'], recipe.link)
        self.assertEqual(len(tags), 0)
