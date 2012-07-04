#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, DiacriticCharacter, SpacingCharacter, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.character import Character
from zounds.constants import BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.exceptions import InvalidCharacterError
from zounds.normalised_form import NormalisedForm


class CharacterTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()
        Character._cache = {}

    def test_delete (self):
        self.assertEqual(len(Character._cache), 0)
        feature = BaseFeature(self.bfm, 'voiced')
        character = BaseCharacter(self.bfm, 'a')
        character.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE),
                         set([character]))
        self.assertEqual(len(Character._cache), 1)
        character.delete()
        self.assertEqual(len(Character._cache), 0)
        self.assertEqual(feature.get_value_characters(HAS_FEATURE), set())

    def test_ipa (self):
        character = BaseCharacter(self.bfm, 'a')
        self.assertEqual(character.ipa, 'a')
        # The IPA form of a character may be set.
        character.ipa = 'b'
        self.assertEqual(character.ipa, 'b')
        # IPA forms must be unique across all characters in a binary
        # features model.
        character2 = SuprasegmentalCharacter(self.bfm, 'a')
        self.assertRaises(InvalidCharacterError, setattr, character2, 'ipa',
                          'b')
        # Setting the IPA form to the existing form should not raise
        # an error.
        character2.ipa = 'a'
        self.assertEqual(character2.ipa, 'a')
        # The IPA form of a character must be a single character.
        self.assertRaises(InvalidCharacterError, BaseCharacter, self.bfm,
                          '')
        self.assertRaises(InvalidCharacterError, BaseCharacter, self.bfm,
                          'ab')
        self.assertRaises(InvalidCharacterError, setattr, character2, 'ipa',
                          'ab')

    def test_normalised_form (self):
        feature1 = BaseFeature(self.bfm, 'anterior')
        character1 = DiacriticCharacter(self.bfm, 'a')
        character1.set_feature_value(feature1, HAS_FEATURE)
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}'.format(BNFM, HAS_FEATURE)))
        # Adding a feature changes the normalised form.
        feature2 = BaseFeature(self.bfm, 'dental')
        character1.set_feature_value(feature2, INAPPLICABLE_FEATURE)
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}{2}'.format(BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE)))
        # The order of the normalised form feature values is
        # alphabetical by feature name.
        feature3 = BaseFeature(self.bfm, 'consonantal')
        character1.set_feature_value(feature3, NOT_HAS_FEATURE)
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}{2}{3}'.format(BNFM, HAS_FEATURE, NOT_HAS_FEATURE,
                                      INAPPLICABLE_FEATURE)))
        # Renaming a feature may change the normalised form.
        feature1.name = 'vocalic'
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}{2}{3}'.format(BNFM, NOT_HAS_FEATURE,
                                      INAPPLICABLE_FEATURE, HAS_FEATURE)))
        # Changing a feature value changes the normalised form.
        character1.set_feature_value(feature1, NOT_HAS_FEATURE)
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}{2}{1}'.format(BNFM, NOT_HAS_FEATURE,
                                      INAPPLICABLE_FEATURE)))
        # Removing a feature value changes the normalised form.
        feature2.delete()
        self.assertEqual(character1.normalised_form, NormalisedForm(
                '{0}{1}{1}'.format(BNFM, NOT_HAS_FEATURE)))

    def test_object_caching (self):
        # Creating a Character with the same IPA form as an existing
        # Character must return the existing Character, if both are
        # associated with the same BinaryFeaturesModel.
        character1 = BaseCharacter(self.bfm, 'a')
        character2 = BaseCharacter(self.bfm, 'a')
        self.assertEqual(character1, character2)
        character3 = BaseCharacter(self.bfm, 'b')
        self.assertNotEqual(character1, character3)
        bfm2 = BinaryFeaturesModel()
        character4 = BaseCharacter(bfm2, 'a')
        self.assertNotEqual(character1, character4)
        # It is an error to create a Character with the same IPA form
        # but of a different type (subclass).
        self.assertRaises(InvalidCharacterError, DiacriticCharacter,
                          self.bfm, 'a')
        # Initialising of the Character should happen only once.
        feature = BaseFeature(self.bfm, 'voiced')
        character1.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(character1.get_feature_value(feature), HAS_FEATURE)
        character5 = BaseCharacter(self.bfm, 'a')
        self.assertEqual(character1.get_feature_value(feature), HAS_FEATURE)
        character6 = DiacriticCharacter(self.bfm, 'c')
        character6.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(character6.get_feature_value(feature), HAS_FEATURE)
        character7 = DiacriticCharacter(self.bfm, 'c')
        self.assertEqual(character6.get_feature_value(feature), HAS_FEATURE)
        character8 = SpacingCharacter(self.bfm, 'd')
        character8.set_feature_value(feature, HAS_FEATURE)
        self.assertEqual(character8.get_feature_value(feature), HAS_FEATURE)
        character9 = SpacingCharacter(self.bfm, 'd')
        self.assertEqual(character8.get_feature_value(feature), HAS_FEATURE)
        character10 = SuprasegmentalCharacter(self.bfm, 'e')
        feature2 = SuprasegmentalFeature(self.bfm, 'syllabic')
        character10.set_feature_value(feature2, HAS_FEATURE)
        self.assertEqual(character10.get_feature_value(feature2), HAS_FEATURE)
        character11 = SuprasegmentalCharacter(self.bfm, 'e')
        self.assertEqual(character10.get_feature_value(feature2), HAS_FEATURE)


if __name__ == '__main__':
    unittest.main()
