#!/usr/bin/env python3

import unittest

from zounds import BaseFeature, BaseFeatureSet, BinaryFeaturesModel, SuprasegmentalFeature
from zounds.constants import AFM, BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.exceptions import MismatchedTypesError
from zounds.normalised_form import NormalisedForm


class BaseFeatureSetTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()
        self.anterior = BaseFeature(self.bfm, 'anterior')
        self.back = BaseFeature(self.bfm, 'back')
        self.coronal = BaseFeature(self.bfm, 'coronal')
        self.long = BaseFeature(self.bfm, 'long')
        self.voiced = BaseFeature(self.bfm, 'voiced')

    def test_applier_form (self):
        bfs = BaseFeatureSet(self.bfm)
        af1 = '{0}{1}{2}{2}{2}{2}{2}'.format(AFM, BNFM, INAPPLICABLE_FEATURE)
        self.assertEqual(bfs.applier_form, af1)
        bfs.set(self.anterior, HAS_FEATURE)
        af2 = '{0}{1}{2}{3}{3}{3}{3}'.format(AFM, BNFM, HAS_FEATURE,
                                             INAPPLICABLE_FEATURE)
        self.assertEqual(bfs.applier_form, af2)
        bfs.set(self.long, NOT_HAS_FEATURE)
        af3 = '{0}{1}{2}{3}{3}{4}{3}'.format(AFM, BNFM, HAS_FEATURE,
                                             INAPPLICABLE_FEATURE,
                                             NOT_HAS_FEATURE)
        self.assertEqual(bfs.applier_form, af3)
        bfs.set(self.anterior, None)
        af4 = '{0}{1}{3}{3}{3}{4}{3}'.format(AFM, BNFM, HAS_FEATURE,
                                             INAPPLICABLE_FEATURE,
                                             NOT_HAS_FEATURE)
        self.assertEqual(bfs.applier_form, af4)
        # QAZ: homorganic variables as feature values

    def test_normalised_form (self):
        bfs = BaseFeatureSet(self.bfm)
        nf1 = NormalisedForm('{0}{1}{1}{1}{1}{1}'.format(
                BNFM, INAPPLICABLE_FEATURE))
        self.assertEqual(bfs.normalised_form, nf1)
        bfs.set(self.anterior, HAS_FEATURE)
        nf2 = NormalisedForm('{0}{1}{2}{2}{2}{2}'.format(
                BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE))
        self.assertEqual(bfs.normalised_form, nf2)
        bfs.set(self.long, NOT_HAS_FEATURE)
        nf3 = NormalisedForm('{0}{1}{2}{2}{3}{2}'.format(
                BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(bfs.normalised_form, nf3)
        bfs.set(self.anterior, None)
        nf4 = NormalisedForm('{0}{2}{2}{2}{3}{2}'.format(
                BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(bfs.normalised_form, nf4)
        # QAZ: homorganic variables as feature values

    def test_set_illegal (self):
        stressed = SuprasegmentalFeature(self.bfm, 'stressed')
        bfs = BaseFeatureSet(self.bfm)
        self.assertRaises(MismatchedTypesError, bfs.set, stressed, HAS_FEATURE)


if __name__ == '__main__':
    unittest.main()
