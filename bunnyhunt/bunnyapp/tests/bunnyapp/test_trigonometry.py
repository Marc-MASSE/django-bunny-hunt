import unittest

from django.test import TestCase
from bunnyapp.controller.bunnyapp.trigonometry import distance, hunter_blind_spot, is_rabbit_hidden


class TrigonometryTest(TestCase):
    def test_distance(self):
        self.assertEqual(distance(0, 0, 3, 4), 5.0)
        self.assertEqual(distance(1, 1, 1, 1), 0.0)

    def test_hunter_blind_spot(self):
        # places=6 means that the expected value is with a precision of 6 decimal places after the decimal point.
        self.assertAlmostEqual(hunter_blind_spot(0, 0, 3, 4), 0.3805064, places=6)
        self.assertAlmostEqual(hunter_blind_spot(1, 1, 2, 2), 0.9553166, places=6)

    def test_is_rabbit_hidden(self):
        self.assertTrue(is_rabbit_hidden(0, 0, 6, 8, 3, 4))
        self.assertFalse(is_rabbit_hidden(0, 0, 2, 2, 3, 4))


if __name__ == '__main__':
    unittest.main()
