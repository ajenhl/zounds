#!/usr/bin/env python3

import unittest

from zounds import BinaryFeaturesModel, Language, Ruleset


class RulesetTestCase (unittest.TestCase):

    def setUp (self):
        super().setUp()
        self.binary_features_model = BinaryFeaturesModel()
        self.ruleset = Ruleset(self.binary_features_model)
    
    def test_languages (self):
        self.assertEqual(len(self.ruleset.languages), 0)
        language1 = Language(self.ruleset, 'English')
        self.assertEqual(len(self.ruleset.languages), 1)
        self.assertTrue(language1 in self.ruleset.languages)
        language2 = Language(self.ruleset, 'German')
        self.assertEqual(len(self.ruleset.languages), 2)
        self.assertEqual(self.ruleset.languages, [language1, language2])
        language3 = Language(self.ruleset, 'Arabic')
        self.assertEqual(len(self.ruleset.languages), 3)
        self.assertEqual(self.ruleset.languages, [language3, language1,
                                                  language2])
        language1.delete()
        self.assertEqual(len(self.ruleset.languages), 2)
        self.assertEqual(self.ruleset.languages, [language3, language2])
        language2.delete()
        language3.delete()
        self.assertEqual(len(self.ruleset.languages), 0)


if __name__ == '__main__':
    unittest.main()
