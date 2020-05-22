from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from core.models import Tag
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
            password='jddkjdj@1k1k'
        )
        Tag.objects.create(user=user2, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Non Veg')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
