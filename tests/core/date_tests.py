#!/usr/bin/env python3

import unittest

from zounds import BinaryFeaturesModel, Date, Ruleset
from zounds.exceptions import IllegalArgumentError


class DateTestCase (unittest.TestCase):

    def setUp (self):
        super().setUp()
        self.binary_features_model = BinaryFeaturesModel()
        self.ruleset = Ruleset(self.binary_features_model)

    def test_number (self):
        date = Date(self.ruleset, 1, '1 A.D.')
        self.assertEqual(date.number, 1)
        date.number = 2
        self.assertEqual(date.number, 2)

    def test_invalid_number (self):
        date1 = Date(self.ruleset, 1, '1 A.D.')
        self.assertRaises(IllegalArgumentError, Date, self.ruleset, 1, '2 A.D.')
        date2 = Date(self.ruleset, 2, '2 A.D.')
        self.assertRaises(IllegalArgumentError, setattr, date2, 'number', 1)
        # Changing a number should make it possible for the old number
        # to be used by a different date.
        date2.number = 3
        date1.number = 2
        # A newly set number must also be unavailable to other dates.
        self.assertRaises(IllegalArgumentError, setattr, date2, 'number', 2)

    def test_name (self):
        date = Date(self.ruleset, 1, '1 A.D.')
        self.assertEqual(date.name, '1 A.D.')
        date.name = '2 A.D.'
        self.assertEqual(date.name, '2 A.D.')

    def test_invalid_name (self):
        date1 = Date(self.ruleset, 1, '1 A.D.')
        self.assertRaises(IllegalArgumentError, Date, self.ruleset, 2, '1 A.D.')
        date2 = Date(self.ruleset, 2, '2 A.D.')
        self.assertRaises(IllegalArgumentError, setattr, date2, 'name',
                          '1 A.D.')
        # Changing a name should make it possible for the old name to
        # be used by a different date.
        date2.name = '3 A.D.'
        date1.name = '2 A.D.'
        # A newly set name must also be unavailable to other dates.
        self.assertRaises(IllegalArgumentError, setattr, date2, 'name',
                          '2 A.D.')
  

if __name__ == '__main__':
    unittest.main()
