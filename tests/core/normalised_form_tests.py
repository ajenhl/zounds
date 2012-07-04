#!/usr/bin/env python3

import unittest

from zounds.base_normalised_form import BaseNormalisedForm
from zounds.constants import BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE, SNFM
from zounds.exceptions import IllegalArgumentError, NormalisedFormValueError
from zounds.normalised_form import NormalisedForm
from zounds.suprasegmental_normalised_form import SuprasegmentalNormalisedForm


class NormalisedFormTestCase (unittest.TestCase):

    def test_subclass (self):
        nf1 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertTrue(isinstance(nf1, BaseNormalisedForm))
        nf2 = NormalisedForm(SNFM + NOT_HAS_FEATURE)
        self.assertTrue(isinstance(nf2, SuprasegmentalNormalisedForm))
    
    def test_addition (self):
        nf1 = NormalisedForm(BNFM + '{0}{0}{0}{1}{1}{1}{2}{2}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        nf2 = NormalisedForm(BNFM + '{0}{1}{2}{0}{1}{2}{0}{1}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        nf1plus2 = NormalisedForm(BNFM + '{0}{1}{0}{0}{1}{1}{0}{1}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        nf2plus1 = NormalisedForm(BNFM + '{0}{0}{0}{1}{1}{1}{0}{1}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        self.assertEqual(nf1 + nf2, nf1plus2)
        self.assertEqual(nf2 + nf1, nf2plus1)

    def test_illegal_addition (self):
        nf1 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertRaises(TypeError, nf1.__add__, 1)
        self.assertRaises(TypeError, 'a'.__add__, nf1)
        nf2 = NormalisedForm(SNFM + NOT_HAS_FEATURE)
        self.assertRaises(TypeError, nf1.__add__, nf2)
        nf3 = NormalisedForm(BNFM + '{0}{0}'.format(NOT_HAS_FEATURE))
        self.assertRaises(NormalisedFormValueError, nf1.__add__, nf3)

    def test_containment (self):
        nf1 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertTrue(HAS_FEATURE in nf1)
        self.assertFalse(NOT_HAS_FEATURE in nf1)

    def test_illegal_creation (self):
        self.assertRaises(IllegalArgumentError, NormalisedForm, 'foo')

    def test_equality (self):
        nf1 = NormalisedForm(BNFM + HAS_FEATURE)
        nf2 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertEqual(nf1, nf2)
        nf3 = NormalisedForm(SNFM + HAS_FEATURE)
        self.assertNotEqual(nf1, nf3)
        nf4 = NormalisedForm(BNFM + NOT_HAS_FEATURE)
        self.assertNotEqual(nf1, nf4)

    def test_subtraction (self):
        nf1 = NormalisedForm(BNFM + '{0}{0}{0}{1}{1}{1}{2}{2}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        nf2 = NormalisedForm(BNFM + '{0}{1}{0}{0}{1}{1}{0}{1}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        nf2minus1 = NormalisedForm(BNFM + '{2}{1}{2}{0}{2}{2}{0}{1}{2}'.format(
                NOT_HAS_FEATURE, HAS_FEATURE, INAPPLICABLE_FEATURE))
        self.assertEqual(nf2 - nf1, nf2minus1)

    def test_subtraction_illegal (self):
        nf1 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertRaises(TypeError, nf1.__sub__, 1)
        self.assertRaises(TypeError, nf1.__sub__, 'a')
        nf2 = NormalisedForm(SNFM + NOT_HAS_FEATURE)
        self.assertRaises(TypeError, nf1.__sub__, nf2)
        nf3 = NormalisedForm(BNFM + '{0}{0}'.format(NOT_HAS_FEATURE))
        self.assertRaises(NormalisedFormValueError, nf1.__sub__, nf3)
        nf4 = NormalisedForm(BNFM + INAPPLICABLE_FEATURE)
        nf5 = NormalisedForm(BNFM + HAS_FEATURE)
        self.assertRaises(NormalisedFormValueError, nf4.__sub__, nf5)
        

if __name__ == '__main__':
    unittest.main()
