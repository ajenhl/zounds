#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, SuprasegmentalCharacter, SuprasegmentalFeature
from zounds.base_cluster import BaseCluster
from zounds.cluster import Cluster
from zounds.constants import BNFM, HAS_FEATURE, SNFM
from zounds.exceptions import IllegalArgumentError
from zounds.normalised_form import NormalisedForm
from zounds.suprasegmental_cluster import SuprasegmentalCluster


class ClusterTestCase (unittest.TestCase):

    def test_normalised_form_cluster_creation (self):
        # Test that the correct subclass of Cluster is created from a
        # normalised form.
        bfm = BinaryFeaturesModel()
        feature1 = BaseFeature(bfm, 'anterior')
        feature2 = SuprasegmentalFeature(bfm, 'long')
        character1 = BaseCharacter(bfm, 'a')
        character1.set_feature_value(feature1, HAS_FEATURE)
        character2 = SuprasegmentalCharacter(bfm, 'b')
        character2.set_feature_value(feature2, HAS_FEATURE)
        nf1 = NormalisedForm('{}{}'.format(BNFM, HAS_FEATURE))
        nf2 = NormalisedForm('{}{}'.format(SNFM, HAS_FEATURE))
        cluster1 = Cluster(bfm, normalised_form=nf1)
        cluster2 = Cluster(bfm, normalised_form=nf2)
        self.assertTrue(isinstance(cluster1, BaseCluster))
        self.assertTrue(isinstance(cluster2, SuprasegmentalCluster))
        self.assertRaises(IllegalArgumentError, Cluster, '')


if __name__ == '__main__':
    unittest.main()
