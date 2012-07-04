#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, DiacriticCharacter, SpacingCharacter
from zounds.constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.exceptions import MismatchedModelsError
from zounds.feature import Feature


class BaseFeatureTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()

    def test_delete (self):
        Feature._cache = {}
        self.assertEqual(len(Feature._cache), 0)
        feature = BaseFeature(self.bfm, 'voiced')
        character = BaseCharacter(self.bfm, 'a')
        character.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(len(Feature._cache), 1)
        self.assertEqual(character.get_feature_value(feature), HAS_FEATURE)
        feature.delete()
        self.assertEqual(len(Feature._cache), 0)
        self.assertRaises(MismatchedModelsError, character.get_feature_value,
                          feature)
        feature = BaseFeature(self.bfm, 'voiced')
        character = SpacingCharacter(self.bfm, 'b')
        self.assertEqual(len(Feature._cache), 1)
        feature.delete()
        self.assertEqual(len(Feature._cache), 0)

    def test_value_characters (self):
        feature = BaseFeature(self.bfm, 'voiced')
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE), set())
        character1 = BaseCharacter(self.bfm, 'a')
        character1.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE),
                         set([character1]))
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE), set())
        character1.set_feature_value(feature, NOT_HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE),
                         set([character1]))
        character2 = DiacriticCharacter(self.bfm, 'b')
        character2.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE),
                         set([character2]))
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE),
                         set([character1]))
        character2.set_feature_value(feature, INAPPLICABLE_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE),
                         set([character1]))
        character3 = SpacingCharacter(self.bfm, 'c')
        character3.set_feature_value(feature, NOT_HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())
        self.assertEqual(feature.get_value_characters(NOT_HAS_FEATURE),
                         set([character1, character3]))
        

if __name__ == '__main__':
    unittest.main()
