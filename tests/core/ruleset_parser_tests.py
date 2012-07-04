#!/usr/bin/env python3

import unittest

from zounds.base_character import BaseCharacter
from zounds.binary_features_model_parser import BinaryFeaturesModelParser
from zounds.base_cluster import BaseCluster
from zounds.ruleset_parser import RulesetParser


class RulesetTestCase (unittest.TestCase):

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
        self.parser = RulesetParser(self.bfm)

    def test_ruleset (self):
        configuration = '''
          [Language Latin]
            [Date 1 1 A.D.]
              Rule a/b/_
          '''
        ruleset = self.parser.parse(configuration)
        self.assertEqual(len(ruleset.languages), 1)
        language = ruleset.languages[0]
        self.assertEqual(language.name, 'Latin')
        self.assertEqual(len(language.dates), 1)
        date = language.dates[0]
        self.assertEqual(date.name, '1 A.D.')
        self.assertEqual(date.number, 1)
        rules = ruleset.get_rules(language, date)
        self.assertEqual(len(rules), 1)
        rule = rules[0]
        self.assertEqual(rule.language, language)
        self.assertEqual(rule.date, date)
        a = BaseCharacter(self.bfm, 'a')
        cluster = BaseCluster(self.bfm, base_character=a)
        pattern = r'(?P<start>)(?P<match>{})(?=)'.format(cluster.applier_form)
        self.assertEqual(rule.applier_form.pattern, pattern)


if __name__ == '__main__':
    unittest.main()
