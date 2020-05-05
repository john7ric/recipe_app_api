from django.test import TestCase
from app.calc import add, substract


class TestCalc(TestCase):
    """ test for adding two numbers together """
    def test_add(self):
        self.assertEqual(add(3, 8), 11)

    def test_substract(self):
        self.assertEqual(substract(4, 2), 2)
