#!/usr/bin/env python3

import unittest

from zounds import BinaryFeaturesModel, BaseFeature, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE, SNFM
from zounds.exceptions import IllegalArgumentError, InvalidCharacterError, MismatchedTypesError, MismatchedModelsError
from zounds.normalised_form import NormalisedForm


class BaseCharacterTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()

    def test_feature_value (self):
        character = SuprasegmentalCharacter(self.bfm, 'a')
        feature = SuprasegmentalFeature(self.bfm, 'voiced')
        character.set_feature_value(feature, HAS_FEATURE)
        value = character.get_feature_value(feature)
        self.assertEqual(value, HAS_FEATURE)
        character.set_feature_value(feature, NOT_HAS_FEATURE)
        value = character.get_feature_value(feature)
        self.assertEqual(value, NOT_HAS_FEATURE)
    
    def test_feature_value_illegal (self):
        # The Feature must belong to the same BinaryFeaturesModel as
        # the Character.
        character = SuprasegmentalCharacter(self.bfm, 'a')
        bfm2 = BinaryFeaturesModel()
        feature1 = SuprasegmentalFeature(bfm2, 'voiced')
        self.assertRaises(MismatchedModelsError, character.get_feature_value,
                          feature1)
        self.assertRaises(MismatchedModelsError, character.set_feature_value,
                          feature1, HAS_FEATURE)
        # The Feature's type (subclass) must be appropriate to the
        # type (subclass) of the Character.
        feature2 = BaseFeature(self.bfm, 'stressed')
        self.assertRaises(MismatchedTypesError, character.get_feature_value,
                          feature2)
        self.assertRaises(MismatchedTypesError, character.set_feature_value,
                          feature2, HAS_FEATURE)
        # A SuprasegmentalCharacter must have a feature value for all
        # SuprasegmentalFeatures.
        feature3 = SuprasegmentalFeature(self.bfm, 'syllabic')
        self.assertRaises(InvalidCharacterError, character.get_feature_value,
                          feature3)
        # Only certain values are permitted.
        self.assertRaises(IllegalArgumentError, character.set_feature_value,
                          feature3, True)

    def test_normalised_form (self):
        feature1 = SuprasegmentalFeature(self.bfm, 'anterior')
        character = SuprasegmentalCharacter(self.bfm, 'n')
        character.set_feature_value(feature1, HAS_FEATURE)
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{1}'.format(SNFM, HAS_FEATURE)))
        # Adding a feature changes the normalised form.
        feature2 = SuprasegmentalFeature(self.bfm, 'dental')
        # All features must have a value.
        self.assertRaises(InvalidCharacterError, getattr, character,
                          'normalised_form')
        character.set_feature_value(feature2, NOT_HAS_FEATURE)
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{1}{2}'.format(SNFM, HAS_FEATURE, NOT_HAS_FEATURE)))
        # The order of the normalised form feature values is
        # alphabetical by feature name.
        feature3 = SuprasegmentalFeature(self.bfm, 'consonantal')
        character.set_feature_value(feature3, HAS_FEATURE)
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{1}{1}{2}'.format(SNFM, HAS_FEATURE, NOT_HAS_FEATURE)))
        # Renaming a feature may change the normalised form.
        feature3.name = 'vocalic'
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{1}{2}{1}'.format(SNFM, HAS_FEATURE, NOT_HAS_FEATURE)))
        # Changing a feature value changes the normalised form.
        character.set_feature_value(feature1, INAPPLICABLE_FEATURE)
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{3}{2}{1}'.format(SNFM, HAS_FEATURE, NOT_HAS_FEATURE,
                                      INAPPLICABLE_FEATURE)))
        # Removing a feature value changes the normalised form.
        feature3.delete()
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{2}{1}'.format(SNFM, NOT_HAS_FEATURE,
                                   INAPPLICABLE_FEATURE)))
        # Adding a feature of a different type does not change the
        # normalised form.
        feature4 = BaseFeature(self.bfm, 'syllabic')
        self.assertEqual(character.normalised_form, NormalisedForm(
                '{0}{2}{1}'.format(SNFM, NOT_HAS_FEATURE,
                                   INAPPLICABLE_FEATURE)))
        

if __name__ == '__main__':
    unittest.main()
