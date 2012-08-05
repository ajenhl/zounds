#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseCluster, BaseFeatureSet, Group, Optional
from zounds.constants import AFM, BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.binary_features_model_parser import BinaryFeaturesModelParser
from zounds.exceptions import IllegalArgumentError, MismatchedModelsError


class GroupTestCase (unittest.TestCase):

    def setUp (self):
        super().setUp()
        bfm_configuration = '''
        [Base Features] anterior consonantal voiced
        [Base Characters] a: anterior b: c: anterior, voiced
        [Diacritic Characters] ̬: +voiced
        '''
        self.bfm = BinaryFeaturesModelParser().parse(bfm_configuration)

    def test_applier_form (self):
        group = Group(self.bfm, 1)
        feature_set = BaseFeatureSet(self.bfm)
        feature_set_form = '{0}{1}{2}{2}{2}'.format(AFM, BNFM,
                                                    INAPPLICABLE_FEATURE)
        self.assertEqual(feature_set.applier_form, feature_set_form)
        group.append(feature_set)
        expected = '(?P<group1>{})'.format(feature_set_form)
        self.assertEqual(group.applier_form, expected)
        c = BaseCharacter(self.bfm, 'c')
        cluster = BaseCluster(self.bfm, base_character=c)
        optional = Optional(self.bfm)
        optional.append(cluster)
        optional_form = '({0}{1}{2}{3}{2})?'.format(AFM, BNFM, HAS_FEATURE,
                                                    NOT_HAS_FEATURE)
        self.assertEqual(optional.applier_form, optional_form)
        group.append(optional)
        expected = '(?P<group1>{}{})'.format(feature_set_form, optional_form)
        self.assertEqual(group.applier_form, expected)

    def test_illegal_append (self):
        group1 = Group(self.bfm, 1)
        group2 = Group(self.bfm, 2)
        self.assertRaises(IllegalArgumentError, group1.append, group2)
        bfm2_configuration = '''
        [Base Features] anterior consonantal voiced
        [Base Characters] a: anterior'''
        bfm2 = BinaryFeaturesModelParser().parse(bfm2_configuration)
        optional = Optional(bfm2)
        self.assertRaises(MismatchedModelsError, group1.append, optional)


if __name__ == '__main__':
    unittest.main()
