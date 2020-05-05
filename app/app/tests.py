from django.test import TestCase
from app.calc import add_numbers


class TestCalc(TestCase):
    """ test for adding two numbers together """
    def test_add(self):
        self.assertEqual(add_numbers(3, 8), 11)
