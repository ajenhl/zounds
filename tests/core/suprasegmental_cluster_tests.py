#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BinaryFeaturesModel, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.cluster import Cluster
from zounds.constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NFM, NOT_HAS_FEATURE, SNFM
from zounds.exceptions import IllegalArgumentError, MismatchedModelsError, MismatchedTypesError
from zounds.normalised_form import NormalisedForm
from zounds.suprasegmental_cluster import SuprasegmentalCluster


class ClusterTestCase (unittest.TestCase):

    def setUp (self):
        self.bfm = BinaryFeaturesModel()
        self.phrase = SuprasegmentalFeature(self.bfm, 'phrase')
        self.stressed = SuprasegmentalFeature(self.bfm, 'stressed')
        self.syllabic = SuprasegmentalFeature(self.bfm, 'syllabic')
        self.a = SuprasegmentalCharacter(self.bfm, 'a')
        self.a.set_feature_value(self.phrase, HAS_FEATURE)
        self.a.set_feature_value(self.stressed, INAPPLICABLE_FEATURE)
        self.a.set_feature_value(self.syllabic, NOT_HAS_FEATURE)
        self.b = SuprasegmentalCharacter(self.bfm, 'b')
        self.b.set_feature_value(self.phrase, INAPPLICABLE_FEATURE)
        self.b.set_feature_value(self.stressed, NOT_HAS_FEATURE)
        self.b.set_feature_value(self.syllabic, INAPPLICABLE_FEATURE)

    def test_applier_form (self):
        cluster1 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a])
        af1 = '{0}{1}{2}{3}{4}'.format(NFM, SNFM, HAS_FEATURE,
                                       INAPPLICABLE_FEATURE, NOT_HAS_FEATURE)
        self.assertEqual(cluster1.applier_form, af1)
        cluster2 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a, self.b])
        af2 = '{0}{1}{2}{3}{3}'.format(NFM, SNFM, HAS_FEATURE, NOT_HAS_FEATURE)
        self.assertEqual(cluster2.applier_form, af2)
    
    def test_normalised_form (self):
        cluster1 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a])
        nf1 = NormalisedForm('{0}{1}{2}{3}'.format(
                SNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(cluster1.normalised_form, nf1)
        cluster2 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a, self.b])
        nf2 = NormalisedForm('{0}{1}{2}{2}'.format(
                SNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(cluster2.normalised_form, nf2)
        cluster3 = Cluster(self.bfm, normalised_form=nf2)
        self.assertEqual(cluster3.normalised_form, nf2)

    def test_string_form (self):
        cluster1 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a])
        self.assertEqual(str(cluster1), 'a')
        cluster2 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.a, self.b])
        self.assertEqual(str(cluster2), 'ab')
        cluster3 = SuprasegmentalCluster(self.bfm, suprasegmental_characters=
                                         [self.b, self.a])
        self.assertEqual(str(cluster3), 'ba')
        
    def test_suprasegmental_cluster_creation_illegal (self):
        bfm1 = BinaryFeaturesModel()
        bfm2 = BinaryFeaturesModel()
        character1 = BaseCharacter(bfm1, 'a')
        character3 = SuprasegmentalCharacter(bfm1, 'b')
        character4 = SuprasegmentalCharacter(bfm2, 'c')
        nf1 = NormalisedForm('{}{}'.format(SNFM, HAS_FEATURE))
        # A SuprasegmentalCluster must be initialised with at least
        # one suprasegmental character or a normalised form.
        self.assertRaises(IllegalArgumentError, SuprasegmentalCluster, bfm1)
        # A SuprasegmentalCluster must not be initialised with both
        # suprasegmental characters and a normalised form.
        self.assertRaises(IllegalArgumentError, SuprasegmentalCluster, bfm1,
                          suprasegmental_characters=[character3],
                          normalised_form=nf1)
        # All of the characters in a cluster must be associated with
        # the same binary features model.
        self.assertRaises(MismatchedModelsError, SuprasegmentalCluster, bfm1,
                          suprasegmental_characters=[character4])
        # All of the characters in a cluster must be suprasegmental.
        self.assertRaises(MismatchedTypesError, SuprasegmentalCluster, bfm1,
                          suprasegmental_characters=[character1, character3])


if __name__ == '__main__':
    unittest.main()
