from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class TestPublicTagAPI(TestCase):
    """
    Testing public API for tags
    """
    def Setup(self):
        self.client = APIClient()

    def test_listing_tags_need_authentication(self):
        """
        testing tags listign without authentication
        """

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateTagsAPI(TestCase):
    """
    Testing tags api components needs autentication
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@mail.com',
            name='Test User',
            password='Open@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_tags(self):
        """
        tests api listing tags
        """

        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Non Veg')
        list = Tag.objects.all().order_by('-name')
        data = TagSerializer(list, many=True).data
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)

    def test_user_tags(self):
        """
        test if only logged in users tags are listed
        """
        user2 = get_user_model().objects.create(
            email='lollslsl@hh.com',
            password='jddkjdj@1k1k',
            name='Test User2'
        )
        Tag.objects.create(user=user2, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Non Veg')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_sucessfull(self):
        """
        test if a tag is created successfully with valid credentials
        """
        payload = {'name': 'test tag'}

        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            name=payload['name'],
            user=self.user).exists

        self.assertTrue(exists)

    def test_invalid_tag_create(self):
        """
        test if tag creation fails with null string
        """
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retreived_tags_assigned_to_recipes(self):
        """
        Test only the tags assigned to recipes are retreived
        """
        recipe = Recipe.objects.create(
            user=self.user,
            title='Chicken Soup',
            time_minutes=10,
            price=5.00
        )
        tag_1 = Tag.objects.create(user=self.user, name='Soup')
        tag_2 = Tag.objects.create(user=self.user, name='Chicken')

        recipe.tags.add(tag_1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer_1 = TagSerializer(tag_1)
        serializer_2 = TagSerializer(tag_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)

    def test_retrieve_tags_assignes_unique(self):
        """
        Test tags retrieved are unique and not duplicated
        """
        recipe_1 = Recipe.objects.create(
            user=self.user,
            title='Chicken Soup',
            time_minutes=10,
            price=5.00
        )
        recipe_2 = Recipe.objects.create(
            user=self.user,
            title='Veg Soup',
            time_minutes=10,
            price=5.00
        )
        tag_1 = Tag.objects.create(user=self.user, name='Soup')
        Tag.objects.create(user=self.user, name='Soup')

        recipe_1.tags.add(tag_1)
        recipe_2.tags.add(tag_1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer_1 = TagSerializer(tag_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertIn(serializer_1.data, res.data)
