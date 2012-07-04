#!/usr/bin/env python3

import unittest

from zounds import BinaryFeaturesModel, Date, Language, Ruleset
from zounds.exceptions import IllegalArgumentError


class LanguageTestCase (unittest.TestCase):

    def setUp (self):
        super().setUp()
        self.binary_features_model = BinaryFeaturesModel()
        self.ruleset = Ruleset(self.binary_features_model)

    def test_dates (self):
        language = Language(self.ruleset, 'English')
        self.assertEqual(len(language.dates), 0)
        date1 = Date(self.ruleset, 1, '1 A.D.')
        language.add_date(date1)
        self.assertEqual(language.dates, [date1])
        date2 = Date(self.ruleset, 2, '2 A.D.')
        language.add_date(date2)
        # Dates are ordered.
        self.assertEqual(language.dates, [date1, date2])
        date2.number = -1
        self.assertEqual(language.dates, [date2, date1])
        date2.delete()
        self.assertEqual(language.dates, [date1])
        date1.delete()
        self.assertEqual(len(language.dates), 0)
        
    def test_name (self):
        language = Language(self.ruleset, 'English')
        self.assertEqual(language.name, 'English')
        language.name = 'German'
        self.assertEqual(language.name, 'German')

    def test_invalid_name (self):
        language1 = Language(self.ruleset, 'English')
        self.assertRaises(IllegalArgumentError, Language, self.ruleset,
                          'English')
        language2 = Language(self.ruleset, 'German')
        self.assertRaises(IllegalArgumentError, setattr, language2, 'name',
                          'English')
        # Changing a name should make it possible for the old name to
        # be used by a different language.
        language2.name = 'French'
        language1.name = 'German'
        # A newly set name must also be unavalable to other languages.
        self.assertRaises(IllegalArgumentError, setattr, language2, 'name',
                          'German')


if __name__ == '__main__':
    unittest.main()
