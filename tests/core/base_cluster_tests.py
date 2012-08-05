#!/usr/bin/env python3

import unittest

from zounds import BaseCharacter, BaseFeature, BinaryFeaturesModel, DiacriticCharacter, SpacingCharacter
from zounds.base_cluster import BaseCluster
from zounds.cluster import Cluster
from zounds.constants import AFM, BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from zounds.exceptions import IllegalArgumentError, MismatchedModelsError, MismatchedTypesError
from zounds.normalised_form import NormalisedForm


class ClusterTestCase (unittest.TestCase):

    def setUp (self):
        self._populate_binary_features_model()

    def _populate_binary_features_model (self):
        self.bfm = BinaryFeaturesModel()
        self.anterior = BaseFeature(self.bfm, 'anterior')
        self.back = BaseFeature(self.bfm, 'back')
        self.coronal = BaseFeature(self.bfm, 'coronal')
        self.long = BaseFeature(self.bfm, 'long')
        self.voiced = BaseFeature(self.bfm, 'voiced')
        self.p = BaseCharacter(self.bfm, 'p')
        self.p.set_feature_value(self.anterior, HAS_FEATURE)
        self.p.set_feature_value(self.back, NOT_HAS_FEATURE)
        self.p.set_feature_value(self.coronal, NOT_HAS_FEATURE)
        self.p.set_feature_value(self.long, NOT_HAS_FEATURE)
        self.p.set_feature_value(self.voiced, NOT_HAS_FEATURE)
        self.b = BaseCharacter(self.bfm, 'b')
        self.b.set_feature_value(self.anterior, HAS_FEATURE)
        self.b.set_feature_value(self.back, NOT_HAS_FEATURE)
        self.b.set_feature_value(self.coronal, NOT_HAS_FEATURE)
        self.b.set_feature_value(self.long, NOT_HAS_FEATURE)
        self.b.set_feature_value(self.voiced, HAS_FEATURE)
        self.t = BaseCharacter(self.bfm, 't')
        self.t.set_feature_value(self.anterior, HAS_FEATURE)
        self.t.set_feature_value(self.back, NOT_HAS_FEATURE)
        self.t.set_feature_value(self.coronal, HAS_FEATURE)
        self.t.set_feature_value(self.long, NOT_HAS_FEATURE)
        self.t.set_feature_value(self.voiced, NOT_HAS_FEATURE)
        self.d = BaseCharacter(self.bfm, 'd')
        self.d.set_feature_value(self.anterior, HAS_FEATURE)
        self.d.set_feature_value(self.back, NOT_HAS_FEATURE)
        self.d.set_feature_value(self.coronal, HAS_FEATURE)
        self.d.set_feature_value(self.long, NOT_HAS_FEATURE)
        self.d.set_feature_value(self.voiced, HAS_FEATURE)
        self.q = BaseCharacter(self.bfm, 'q')
        self.q.set_feature_value(self.anterior, NOT_HAS_FEATURE)
        self.q.set_feature_value(self.back, HAS_FEATURE)
        self.q.set_feature_value(self.coronal, NOT_HAS_FEATURE)
        self.q.set_feature_value(self.long, NOT_HAS_FEATURE)
        self.q.set_feature_value(self.voiced, NOT_HAS_FEATURE)
        self.ring = DiacriticCharacter(self.bfm, '̥')
        self.ring.set_feature_value(self.anterior, INAPPLICABLE_FEATURE)
        self.ring.set_feature_value(self.back, INAPPLICABLE_FEATURE)
        self.ring.set_feature_value(self.coronal, INAPPLICABLE_FEATURE)
        self.ring.set_feature_value(self.long, INAPPLICABLE_FEATURE)
        self.ring.set_feature_value(self.voiced, NOT_HAS_FEATURE)
        self.caret = DiacriticCharacter(self.bfm, '̬')
        self.caret.set_feature_value(self.anterior, INAPPLICABLE_FEATURE)
        self.caret.set_feature_value(self.back, INAPPLICABLE_FEATURE)
        self.caret.set_feature_value(self.coronal, INAPPLICABLE_FEATURE)
        self.caret.set_feature_value(self.long, INAPPLICABLE_FEATURE)
        self.caret.set_feature_value(self.voiced, HAS_FEATURE)
        self.ː = SpacingCharacter(self.bfm, 'ː')
        self.ː.set_feature_value(self.anterior, INAPPLICABLE_FEATURE)
        self.ː.set_feature_value(self.back, INAPPLICABLE_FEATURE)
        self.ː.set_feature_value(self.coronal, INAPPLICABLE_FEATURE)
        self.ː.set_feature_value(self.long, HAS_FEATURE)
        self.ː.set_feature_value(self.voiced, INAPPLICABLE_FEATURE)

    def test_resolve_normalised_form (self):
        nf1 = NormalisedForm('{0}{1}{2}{2}{2}{2}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        cluster1 = Cluster(self.bfm, normalised_form=nf1)
        self.assertEqual(cluster1.base_character, self.p)
        self.assertEqual(cluster1.diacritic_characters, [])
        self.assertEqual(cluster1.spacing_characters, [])
        nf2 = NormalisedForm('{0}{2}{1}{2}{2}{1}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        cluster2 = Cluster(self.bfm, normalised_form=nf2)
        self.assertEqual(cluster2.base_character, self.q)
        self.assertEqual(cluster2.diacritic_characters, [self.caret])
        self.assertEqual(cluster2.spacing_characters, [])
        nf3 = NormalisedForm('{0}{2}{1}{2}{1}{1}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        cluster3 = Cluster(self.bfm, normalised_form=nf3)
        self.assertEqual(cluster3.base_character, self.q)
        self.assertEqual(cluster3.diacritic_characters, [self.caret])
        self.assertEqual(cluster3.spacing_characters, [self.ː])

    def test_base_cluster_creation_illegal (self):
        bfm1 = BinaryFeaturesModel()
        bfm2 = BinaryFeaturesModel()
        character1 = BaseCharacter(bfm1, 'a')
        character2 = DiacriticCharacter(bfm2, 'b')
        character3 = DiacriticCharacter(bfm1, 'd')
        character4 = SpacingCharacter(bfm1, 'e')
        nf1 = NormalisedForm('{}{}'.format(BNFM, HAS_FEATURE))
        # A BaseCluster must be initialised with either a base
        # character or a normalised form.
        self.assertRaises(IllegalArgumentError, BaseCluster, bfm1)
        # A BaseCluster must not be initialised with both a normalised
        # form and any other argument.
        self.assertRaises(IllegalArgumentError, BaseCluster, bfm1,
                          base_character=character1, normalised_form=nf1)
        self.assertRaises(IllegalArgumentError, BaseCluster, bfm1,
                          diacritic_characters=[character3],
                          normalised_form=nf1)
        self.assertRaises(IllegalArgumentError, BaseCluster, bfm1,
                          spacing_characters=[character4], normalised_form=nf1)
        # All of the characters in a BaseCluster must be associated with
        # the same binary features model.
        self.assertRaises(MismatchedModelsError, BaseCluster, bfm1,
                          base_character=character1,
                          diacritic_characters=[character2])
        # A BaseCluster expects specific types of characters in its
        # arguments.
        self.assertRaises(MismatchedTypesError, BaseCluster, bfm1,
                          base_character=character3)
        self.assertRaises(MismatchedTypesError, BaseCluster, bfm1,
                          base_character=character1,
                          diacritic_characters=[character4])
        self.assertRaises(MismatchedTypesError, BaseCluster, bfm1,
                          base_character=character1,
                          spacing_characters=[character3])

    def test_applier_form (self):
        cluster1 = BaseCluster(self.bfm, base_character=self.p)
        af1 = '{0}{1}{2}{3}{3}{3}{3}'.format(AFM, BNFM, HAS_FEATURE,
                                             NOT_HAS_FEATURE)
        self.assertEqual(cluster1.applier_form, af1)
        cluster2 = BaseCluster(self.bfm, base_character=self.q,
                           diacritic_characters=[self.caret])
        af2 = '{0}{1}{3}{2}{3}{3}{2}'.format(AFM, BNFM, HAS_FEATURE,
                                             NOT_HAS_FEATURE)
        self.assertEqual(cluster2.applier_form, af2)
        cluster3 = BaseCluster(self.bfm, base_character=self.q,
                               diacritic_characters=[self.caret],
                               spacing_characters=[self.ː])
        af3 = '{0}{1}{3}{2}{3}{2}{2}'.format(AFM, BNFM, HAS_FEATURE,
                                             NOT_HAS_FEATURE)
        self.assertEqual(cluster3.applier_form, af3)

    def test_normalised_form (self):
        cluster1 = BaseCluster(self.bfm, base_character=self.p)
        nf1 = NormalisedForm('{0}{1}{2}{2}{2}{2}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(cluster1.normalised_form, nf1)
        cluster2 = BaseCluster(self.bfm, base_character=self.q,
                           diacritic_characters=[self.caret])
        nf2 = NormalisedForm('{0}{2}{1}{2}{2}{1}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(cluster2.normalised_form, nf2)
        cluster3 = BaseCluster(self.bfm, base_character=self.q,
                               diacritic_characters=[self.caret],
                               spacing_characters=[self.ː])
        nf3 = NormalisedForm('{0}{2}{1}{2}{1}{1}'.format(
                BNFM, HAS_FEATURE, NOT_HAS_FEATURE))
        self.assertEqual(cluster3.normalised_form, nf3)

    def test_string_form (self):
        cluster1 = BaseCluster(self.bfm, base_character=self.p)
        self.assertEqual(str(cluster1), 'p')
        cluster2 = BaseCluster(self.bfm, base_character=self.q,
                           diacritic_characters=[self.caret])
        self.assertEqual(str(cluster2), 'q̬')
        cluster3 = BaseCluster(self.bfm, base_character=self.q,
                               diacritic_characters=[self.caret],
                               spacing_characters=[self.ː])
        self.assertEqual(str(cluster3), 'q̬ː')


if __name__ == '__main__':
    unittest.main()
