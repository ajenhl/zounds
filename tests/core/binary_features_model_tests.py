#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, DiacriticCharacter, SpacingCharacter, SuprasegmentalCharacter, SuprasegmentalFeature


class BinaryFeaturesModelTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()

    def test_analyse_script_string (self):
        pass

    def test_base_characters (self):
        self.assertEqual(len(self.bfm.base_characters), 0)
        character1 = BaseCharacter(self.bfm, 'a')
        self.assertEqual(len(self.bfm.base_characters), 1)
        self.assertTrue(character1 in self.bfm.base_characters)
        character2 = BaseCharacter(self.bfm, 'b')
        self.assertEqual(len(self.bfm.base_characters), 2)
        self.assertTrue(character1 in self.bfm.base_characters)
        self.assertTrue(character2 in self.bfm.base_characters)
        character2.delete()
        self.assertEqual(len(self.bfm.base_characters), 1)
        self.assertTrue(character1 in self.bfm.base_characters)
        character1.delete()
        self.assertEqual(len(self.bfm.base_characters), 0)
        character3 = DiacriticCharacter(self.bfm, 'c')
        self.assertEqual(len(self.bfm.base_characters), 0)

    def test_base_features (self):
        self.assertEqual(len(self.bfm.base_features), 0)
        feature1 = BaseFeature(self.bfm, 'voiced')
        self.assertEqual(len(self.bfm.base_features), 1)
        self.assertTrue(feature1 in self.bfm.base_features)
        feature2 = BaseFeature(self.bfm, 'consonantal')
        self.assertEqual(len(self.bfm.base_features), 2)
        self.assertTrue(feature1 in self.bfm.base_features)
        self.assertTrue(feature2 in self.bfm.base_features)
        feature2.delete()
        self.assertEqual(len(self.bfm.base_features), 1)
        self.assertTrue(feature1 in self.bfm.base_features)
        feature1.delete()
        self.assertEqual(len(self.bfm.base_features), 0)
        feature3 = SuprasegmentalFeature(self.bfm, 'syllabic')
        self.assertEqual(len(self.bfm.base_features), 0)

    def test_diacritic_characters (self):
        self.assertEqual(len(self.bfm.diacritic_characters), 0)
        character1 = DiacriticCharacter(self.bfm, 'a')
        self.assertEqual(len(self.bfm.diacritic_characters), 1)
        self.assertTrue(character1 in self.bfm.diacritic_characters)
        character2 = DiacriticCharacter(self.bfm, 'b')
        self.assertEqual(len(self.bfm.diacritic_characters), 2)
        self.assertTrue(character1 in self.bfm.diacritic_characters)
        self.assertTrue(character2 in self.bfm.diacritic_characters)
        character2.delete()
        self.assertEqual(len(self.bfm.diacritic_characters), 1)
        self.assertTrue(character1 in self.bfm.diacritic_characters)
        character1.delete()
        self.assertEqual(len(self.bfm.diacritic_characters), 0)
        character3 = SpacingCharacter(self.bfm, 'c')
        self.assertEqual(len(self.bfm.diacritic_characters), 0)
    
    def test_spacing_characters (self):
        self.assertEqual(len(self.bfm.spacing_characters), 0)
        character1 = SpacingCharacter(self.bfm, 'a')
        self.assertEqual(len(self.bfm.spacing_characters), 1)
        self.assertTrue(character1 in self.bfm.spacing_characters)
        character2 = SpacingCharacter(self.bfm, 'b')
        self.assertEqual(len(self.bfm.spacing_characters), 2)
        self.assertTrue(character1 in self.bfm.spacing_characters)
        self.assertTrue(character2 in self.bfm.spacing_characters)
        character2.delete()
        self.assertEqual(len(self.bfm.spacing_characters), 1)
        self.assertTrue(character1 in self.bfm.spacing_characters)
        character1.delete()
        self.assertEqual(len(self.bfm.spacing_characters), 0)
        character3 = SuprasegmentalCharacter(self.bfm, 'c')
        self.assertEqual(len(self.bfm.spacing_characters), 0)

    def test_suprasegmental_characters (self):
        self.assertEqual(len(self.bfm.suprasegmental_characters), 0)
        character1 = SuprasegmentalCharacter(self.bfm, 'a')
        self.assertEqual(len(self.bfm.suprasegmental_characters), 1)
        self.assertTrue(character1 in self.bfm.suprasegmental_characters)
        character2 = SuprasegmentalCharacter(self.bfm, 'b')
        self.assertEqual(len(self.bfm.suprasegmental_characters), 2)
        self.assertTrue(character1 in self.bfm.suprasegmental_characters)
        self.assertTrue(character2 in self.bfm.suprasegmental_characters)
        character2.delete()
        self.assertEqual(len(self.bfm.suprasegmental_characters), 1)
        self.assertTrue(character1 in self.bfm.suprasegmental_characters)
        character1.delete()
        self.assertEqual(len(self.bfm.suprasegmental_characters), 0)
        character3 = BaseCharacter(self.bfm, 'c')
        self.assertEqual(len(self.bfm.suprasegmental_characters), 0)
    
    def test_suprasegmental_features (self):
        self.assertEqual(len(self.bfm.suprasegmental_features), 0)
        feature1 = SuprasegmentalFeature(self.bfm, 'voiced')
        self.assertEqual(len(self.bfm.suprasegmental_features), 1)
        self.assertTrue(feature1 in self.bfm.suprasegmental_features)
        feature2 = SuprasegmentalFeature(self.bfm, 'consonantal')
        self.assertEqual(len(self.bfm.suprasegmental_features), 2)
        self.assertTrue(feature1 in self.bfm.suprasegmental_features)
        self.assertTrue(feature2 in self.bfm.suprasegmental_features)
        feature2.delete()
        self.assertEqual(len(self.bfm.suprasegmental_features), 1)
        self.assertTrue(feature1 in self.bfm.suprasegmental_features)
        feature1.delete()
        self.assertEqual(len(self.bfm.suprasegmental_features), 0)
        feature3 = BaseFeature(self.bfm, 'anterior')
        self.assertEqual(len(self.bfm.suprasegmental_features), 0)

    
if __name__ == '__main__':
    unittest.main()
