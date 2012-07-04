#!/usr/bin/env python3

import unittest

from zounds.base_character import BaseCharacter
from zounds.base_cluster import BaseCluster
from zounds.binary_features_model_parser import BinaryFeaturesModelParser
from zounds.context_rule_component import ContextRuleComponent
from zounds.placeholder import Placeholder
from zounds.source_rule_component import SourceRuleComponent


class PlaceholderTestCase (unittest.TestCase):

    def setUp (self):
        bfm_configuration = '''
          [Base Features] anterior consonantal voiced
          [Base Characters] a: anterior b: c: anterior, voiced
          [Diacritic Characters] ̬: +voiced
          [Spacing Characters] ʲ: +consonantal ʰ: -anterior
          [Suprasegmental Features] stressed syllabic
          [Suprasegmental Characters] ˈ: +stressed .: +syllabic
          '''
        self.bfm = BinaryFeaturesModelParser().parse(bfm_configuration)
        self.context_component = ContextRuleComponent()
        self.source_component = SourceRuleComponent()

    def test_placeholder_applier_form (self):
        placeholder = Placeholder(self.bfm, self.source_component)
        self.assertEqual(placeholder.applier_form, ')(?P<match>)(?=')
        a = BaseCharacter(self.bfm, 'a')
        cluster = BaseCluster(self.bfm, base_character=a)
        self.source_component.append(cluster)
        self.assertEqual(placeholder.applier_form,
                         ')(?P<match>{})(?='.format(cluster.applier_form))


if __name__ == '__main__':
    unittest.main()
