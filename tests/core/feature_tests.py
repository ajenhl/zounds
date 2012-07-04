#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.constants import HAS_FEATURE
from zounds.exceptions import InvalidFeatureError


class FeatureTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()

    def test_get_value_characters (self):
        pass

    def test_name (self):
        feature = BaseFeature(self.bfm, 'voiced')
        self.assertEqual(feature.name, 'voiced')
        # Feature names can be set.
        feature.name = 'vocalic'
        self.assertEqual(feature.name, 'vocalic')
        # Feature names must be unique across all features in a binary
        # features model.
        feature2 = SuprasegmentalFeature(self.bfm, 'consonantal')
        self.assertRaises(InvalidFeatureError, setattr, feature2, 'name',
                          'vocalic')
        # Setting the name to the existing name should not raise an error.
        feature2.name = 'consonantal'
        self.assertEqual(feature2.name, 'consonantal')

    def test_object_caching (self):
        # Creating a Feature with the same name as an existing
        # Feature must return the existing Feature, if both are
        # associated with the same BinaryFeaturesModel.
        feature1 = BaseFeature(self.bfm, 'voiced')
        feature2 = BaseFeature(self.bfm, 'voiced')
        self.assertEqual(feature1, feature2)
        feature3 = BaseFeature(self.bfm, 'consonantal')
        self.assertNotEqual(feature1, feature3)
        bfm2 = BinaryFeaturesModel()
        feature4 = BaseFeature(bfm2, 'voiced')
        self.assertNotEqual(feature1, feature4)
        # It is an error to create a Feature with the same IPA form
        # but of a different type (subclass).
        self.assertRaises(InvalidFeatureError, SuprasegmentalFeature, self.bfm,
                          'voiced')
        # Initialisation of a Feature should happen only once.
        character1 = BaseCharacter(self.bfm, 'a')
        character1.set_feature_value(feature1, HAS_FEATURE)
        self.assertEqual(feature1.get_value_characters(HAS_FEATURE),
                         set([character1]))
        feature5 = BaseFeature(self.bfm, 'voiced')
        self.assertEqual(feature1.get_value_characters(HAS_FEATURE),
                         set([character1]))
        feature6 = SuprasegmentalFeature(self.bfm, 'syllabic')
        character2 = SuprasegmentalCharacter(self.bfm, 'b')
        character2.set_feature_value(feature6, HAS_FEATURE)
        self.assertEqual(feature6.get_value_characters(HAS_FEATURE),
                         set([character2]))
        feature7 = SuprasegmentalFeature(self.bfm, 'syllabic')
        self.assertEqual(feature6.get_value_characters(HAS_FEATURE),
                         set([character2]))


if __name__ == '__main__':
    unittest.main()
