#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseCluster, BaseFeature, BaseFeatureSet, Group, Optional
from zounds.binary_features_model_parser import BinaryFeaturesModelParser
from zounds.constants import BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NFM, NOT_HAS_FEATURE
from zounds.exceptions import IllegalArgumentError, MismatchedModelsError


class OptionalTestCase (unittest.TestCase):

    def setUp (self):
        super().setUp()
        bfm_configuration = '''
        [Base Features] anterior consonantal voiced
        [Base Characters] a: anterior b: c: anterior, voiced
        [Diacritic Characters] ̬: +voiced
        '''
        self.bfm = BinaryFeaturesModelParser().parse(bfm_configuration)
        self.optional = Optional(self.bfm)
    
    def test_applier_form (self):
        a = BaseCharacter(self.bfm, 'a')
        cluster1 = BaseCluster(self.bfm, base_character=a)
        cluster1_form = '{0}{1}{2}{3}{3}'.format(NFM, BNFM, HAS_FEATURE,
                                                 NOT_HAS_FEATURE)
        self.optional.append(cluster1)
        expected = '({})?'.format(cluster1_form)
        self.assertEqual(self.optional.applier_form, expected)
        self.optional.match_multiple = True
        expected = '({})*'.format(cluster1_form)
        self.assertEqual(self.optional.applier_form, expected)
        voiced = BaseFeature(self.bfm, 'voiced')
        feature_set = BaseFeatureSet(self.bfm)
        feature_set.set(voiced, HAS_FEATURE)
        feature_set_form = '{0}{1}{2}{2}{3}'.format(
            NFM, BNFM, INAPPLICABLE_FEATURE, HAS_FEATURE)
        self.optional.append(feature_set)
        expected = '({}{})*'.format(cluster1_form, feature_set_form)
        self.assertEqual(self.optional.applier_form, expected)

    def test_illegal_append (self):
        feature_set = BaseFeatureSet(self.bfm)
        self.optional.append(feature_set)
        optional = Optional(self.bfm)
        self.assertRaises(IllegalArgumentError, optional.append, self.optional)
        group = Group(self.bfm, 1)
        self.assertRaises(IllegalArgumentError, optional.append, group)
        bfm2_configuration = '''
        [Base Features] anterior consonantal voiced
        [Base Characters] a: anterior'''
        bfm2 = BinaryFeaturesModelParser().parse(bfm2_configuration)
        a = BaseCharacter(bfm2, 'a')
        cluster = BaseCluster(bfm2, base_character=a)
        self.assertRaises(MismatchedModelsError, self.optional.append, cluster)
        

if __name__ == '__main__':
    unittest.main()
