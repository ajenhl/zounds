#!/usr/bin/env python3

import unittest

from pyparsing import ParseException, ParseFatalException

from zounds import BaseCharacter, BaseFeature, DiacriticCharacter, SpacingCharacter, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.binary_features_model_parser import BinaryFeaturesModelParser
from zounds.constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE


class BinaryFeaturesModelParserTestCase (unittest.TestCase):

    def setUp (self):
        self.parser = BinaryFeaturesModelParser()

    def test_model (self):
        configuration = '''
          [Base Features] anterior low syllabic voiced
          [Base Characters] a: b: anterior c: low, voiced
          [Diacritic Characters] ̥: +anterior
          [Spacing Characters] ʰ: -low, +voiced
          [Suprasegmental Features] phrase stressed
          [Suprasegmental Characters] |: +phrase ˈ: +stressed, +phrase
          '''
        model = self.parser.parse(configuration)
        # Base features.
        self.assertEqual(len(model.base_features), 4)
        anterior = BaseFeature(model, 'anterior')
        low = BaseFeature(model, 'low')
        syllabic = BaseFeature(model, 'syllabic')
        voiced = BaseFeature(model, 'voiced')
        self.assertEqual(len(model.base_features), 4)
        self.assertTrue(anterior in model.base_features)
        self.assertTrue(low in model.base_features)
        self.assertTrue(syllabic in model.base_features)
        self.assertTrue(voiced in model.base_features)
        # Base characters.
        self.assertEqual(len(model.base_characters), 3)
        a = BaseCharacter(model, 'a')
        b = BaseCharacter(model, 'b')
        c = BaseCharacter(model, 'c')
        self.assertEqual(len(model.base_characters), 3)
        self.assertTrue(a in model.base_characters)
        self.assertTrue(b in model.base_characters)
        self.assertTrue(c in model.base_characters)
        # Diacritic characters.
        self.assertEqual(len(model.diacritic_characters), 1)
        ring = DiacriticCharacter(model, '̥')
        self.assertEqual(len(model.diacritic_characters), 1)
        self.assertTrue(ring in model.diacritic_characters)
        # Spacing characters.
        self.assertEqual(len(model.spacing_characters), 1)
        ʰ = SpacingCharacter(model, 'ʰ')
        self.assertEqual(len(model.spacing_characters), 1)
        self.assertTrue(ʰ in model.spacing_characters)
        # Suprasegmental features.
        self.assertEqual(len(model.suprasegmental_features), 2)
        phrase = SuprasegmentalFeature(model, 'phrase')
        stressed = SuprasegmentalFeature(model, 'stressed')
        self.assertEqual(len(model.suprasegmental_features), 2)
        self.assertTrue(phrase in model.suprasegmental_features)
        self.assertTrue(stressed in model.suprasegmental_features)
        # Suprasegmental characters.
        self.assertEqual(len(model.suprasegmental_characters), 2)
        bar = SuprasegmentalCharacter(model, '|')
        ˈ = SuprasegmentalCharacter(model, 'ˈ')
        self.assertEqual(len(model.suprasegmental_characters), 2)
        self.assertTrue(bar in model.suprasegmental_characters)
        self.assertTrue(ˈ in model.suprasegmental_characters)
        # Feature values.
        anterior_has_feature = anterior.get_value_characters(HAS_FEATURE)
        self.assertEqual(len(anterior_has_feature), 2)
        self.assertTrue(b in anterior_has_feature)
        self.assertTrue(ring in anterior_has_feature)
        anterior_not_has_feature = anterior.get_value_characters(
            NOT_HAS_FEATURE)
        self.assertEqual(len(anterior_not_has_feature), 2)
        self.assertTrue(a in anterior_not_has_feature)
        self.assertTrue(c in anterior_not_has_feature)
        anterior_inapplicable_feature = anterior.get_value_characters(
            INAPPLICABLE_FEATURE)
        self.assertEqual(len(anterior_inapplicable_feature), 1)
        self.assertTrue(ʰ in anterior_inapplicable_feature)
        phrase_has_feature = phrase.get_value_characters(HAS_FEATURE)
        self.assertEqual(len(phrase_has_feature), 2)
        self.assertTrue(bar in phrase_has_feature)
        self.assertTrue(ˈ in phrase_has_feature)
        phrase_not_has_feature = phrase.get_value_characters(NOT_HAS_FEATURE)
        self.assertEqual(len(phrase_not_has_feature), 0)
        phrase_inapplicable_feature = phrase.get_value_characters(
            INAPPLICABLE_FEATURE)
        self.assertEqual(len(phrase_inapplicable_feature), 0)

    def test_optional_sections (self):
        # Optional sections should be optional.
        configuration = '''
          [Base Features] anterior low syllabic voiced
          [Base Characters] a: b: anterior c: low, voiced'''
        model = self.parser.parse(configuration)
        self.assertEqual(len(model.base_features), 4)
        anterior = BaseFeature(model, 'anterior')
        low = BaseFeature(model, 'low')
        syllabic = BaseFeature(model, 'syllabic')
        voiced = BaseFeature(model, 'voiced')
        self.assertEqual(len(model.base_features), 4)
        self.assertTrue(anterior in model.base_features)
        self.assertTrue(low in model.base_features)
        self.assertTrue(syllabic in model.base_features)
        self.assertTrue(voiced in model.base_features)
        # Base characters.
        self.assertEqual(len(model.base_characters), 3)
        a = BaseCharacter(model, 'a')
        b = BaseCharacter(model, 'b')
        c = BaseCharacter(model, 'c')
        self.assertEqual(len(model.base_characters), 3)
        self.assertTrue(a in model.base_characters)
        self.assertTrue(b in model.base_characters)
        self.assertTrue(c in model.base_characters)
        # Feature values.
        anterior_has_feature = anterior.get_value_characters(HAS_FEATURE)
        self.assertEqual(len(anterior_has_feature), 1)
        self.assertTrue(b in anterior_has_feature)
        anterior_not_has_feature = anterior.get_value_characters(
            NOT_HAS_FEATURE)
        self.assertEqual(len(anterior_not_has_feature), 2)
        self.assertTrue(a in anterior_not_has_feature)
        self.assertTrue(c in anterior_not_has_feature)
        anterior_inapplicable_feature = anterior.get_value_characters(
            INAPPLICABLE_FEATURE)
        self.assertEqual(len(anterior_inapplicable_feature), 0)

    def test_invalid_base_characters_section (self):
        # Provide a mangled section heading.
        model = '[Base Features] anterior low\n[BaseCharacters] p: anterior'
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character that is not a base character.
        model = '[Base Features] anterior low\n[Base Characters] ʰ: anterior'
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character specifying a non-existent feature.
        model = '''[Base Features] anterior low[Base Characters] p: high'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide the same character twice (a semantic error).
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          p: low'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)
    
    def test_invalid_base_features_section (self):
        # Provide a mangled section heading.
        model = '[BaseFeatures] anterior low\n[Base Characters] p: anterior'
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide no feature names.
        model = '[Base Features]\n[Base Characters] p: anterior'
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a duplicate feature name (a semantic error).
        model = '''[Base Features] anterior anterior low
          [Base Characters] p: anterior'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)

    def test_invalid_diacritic_characters_section (self):
        # Provide a mangled section heading.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [DiacriticCharacters] ̟: +low'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character that is not a diacritic character.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Diacritic Characters] a: +low'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide no feature values.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Diacritic Characters] ̟:'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character specifying a non-existent feature.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Diacritic Characters] ̟: +high'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide the same character twice (a semantic error).
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Diacritic Characters] ̟: +low ̟: -anterior'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)

    def test_invalid_spacing_characters_section (self):
        # Provide a mangled section heading.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [SpacingCharacters] ʰ: +low'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character that is not a spacing character.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Spacing Characters] a: +low'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character specifying a non-existent feature.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Spacing Characters] ʰ: +high'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide the same character twice (a semantic error).
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Spacing Characters] ʰ: +low ʰ: -anterior'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)

    def test_invalid_suprasegmental_features_section (self):
        # Provide a mangled section heading.
        model = '''[Base Features] anterior [Base Characters] p:
          [SuprasegmentalFeatures] stressed [Suprasegmental Characters] ˈ:'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a suprasegmental features section with no
        # suprasegmental characters section.
        model = '''[Base Features] anterior [Base Characters] p:
          [Suprasegmental Features] stressed'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character that is not a suprasegmental character.
        model = '''[Base Features] anterior [Base Characters] p:
          [Suprasegmental Features] stressed [Suprasegmental Characters] a:'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide a character specifying a non-existent feature.
        model = '''[Base Features] anterior [Base Characters] p:
          [Suprasegmental Features] stressed
          [Suprasegmental Characters] ˈ: +anterior'''
        self.assertRaises(ParseException, self.parser.parse, model)
        # Provide the same character twice (a semantic error).
        model = '''[Base Features] anterior [Base Characters] p:
          [Suprasegmental Features] stressed
          [Suprasegmental Characters] ˈ: +stressed ˈ: +stressed'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)
        # Provide the same feature as a base feature (a semantic error).
        model = '''[Base Features] anterior [Base Characters] p:
          [Suprasegmental Features] anterior stressed
          [Suprasegmental Characters] ˈ: +stressed'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)
        
    def test_duplicate_characters (self):
        # Some characters are listed as both suprasegmental and either
        # diacritic or spacing. If such a character is used in one
        # context, it must not be used in the other.
        model = '''[Base Features] anterior low\n[Base Characters] p: anterior
          [Spacing Characters] ː: +low [Suprasegmental Features] long
          [Suprasegmental Characters] ː: +long'''
        self.assertRaises(ParseFatalException, self.parser.parse, model)


if __name__ == '__main__':
    unittest.main()
