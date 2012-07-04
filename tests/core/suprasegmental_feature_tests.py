#!/usr/bin/env python3

import unittest

from zounds import BinaryFeaturesModel, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.exceptions import MismatchedModelsError
from zounds.feature import Feature


class SuprasegmentalFeatureTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()

    def test_delete (self):
        Feature._cache = {}
        self.assertEqual(len(Feature._cache), 0)
        feature = SuprasegmentalFeature(self.bfm, 'voiced')
        character = SuprasegmentalCharacter(self.bfm, 'a')
        character.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(len(Feature._cache), 1)
        self.assertEqual(character.get_feature_value(feature), HAS_FEATURE)
        feature.delete()
        self.assertEqual(len(Feature._cache), 0)
        self.assertRaises(MismatchedModelsError, character.get_feature_value,
                          feature)

    def test_value_characters (self):
        feature = SuprasegmentalFeature(self.bfm, 'voiced')
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE), set())
        character = SuprasegmentalCharacter(self.bfm, 'a')
        character.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE),
                         set([character]))
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE), set())
        character.set_feature_value(feature, NOT_HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE),
                         set([character]))
        character.set_feature_value(feature, INAPPLICABLE_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE), set())
        

if __name__ == '__main__':
    unittest.main()
