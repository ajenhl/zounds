from pyparsing import alphanums, alphas, Combine, Group, Keyword, Literal, nums, OneOrMore, Or, Suppress, Word, ZeroOrMore


from .base_character import BaseCharacter
from .base_cluster import BaseCluster
from .constants import CLOSE_BASE_FEATURE_SET, HOMORGANIC_VARIABLES, OPEN_BASE_FEATURE_SET, RULE_COMPONENT_DIVIDER, SOURCE_PLACEHOLDER
from .context_rule_component import ContextRuleComponent
from .date import Date
from .language import Language
from .placeholder import Placeholder
from .result_rule_component import ResultRuleComponent
from .rule import Rule
from .ruleset import Ruleset
from .source_rule_component import SourceRuleComponent


class RulesetParser:

    """Class for parsing a ruleset configuration and generating a
    `.Ruleset` object."""

    def __init__ (self, binary_features_model):
        """Initialise this object.

        :param binary_features_model: the binary features model to use
          in generating the parser's grammar
        :type binary_features_model: `.BinaryFeaturesModel`

        """
        self._binary_features_model = binary_features_model
        self._grammar = self._define_grammar()
        # Keep track of state.
        self._current_rule_component = SourceRuleComponent()
        self._current_source_component = None

    def _create_date (self, ruleset, language, date_section):
        number = date_section['date_number']
        date_name = date_section['date_name']
        date = Date(ruleset, number, date_name)
        language.add_date(date)
        for rule_data in date_section['rules']:
            self._create_rule(language, date, rule_data)
        
    def _create_language (self, ruleset, language_section):
        language_name = language_section['language_name']
        language = Language(ruleset, language_name)
        for date_section in language_section[1:]:
            self._create_date(ruleset, language, date_section)

    def _create_rule (self, language, date, rule_data):
        source_component = rule_data['source_component']
        context_component = rule_data['context_component']
        result_component = rule_data['result_component']
        rule = Rule(language, date, source_component, context_component,
                    result_component)
            
    def _create_ruleset (self, data):
        ruleset = Ruleset(self._binary_features_model)
        for language_section in data:
            self._create_language(ruleset, language_section)
        return ruleset
        
    def _define_base_feature_set (self):
        open_marker = Literal(OPEN_BASE_FEATURE_SET)
        close_marker = Literal(CLOSE_BASE_FEATURE_SET)
        plus = Literal('+')
        minus = Literal('-') ^ Literal('\N{MINUS SIGN}')
        homorganic_variable = Or([Literal(symbol) for symbol in
                                  HOMORGANIC_VARIABLES])
        #homorganic_variable.setParseAction(self._handle_homorganic_variable)
        feature = Or([Literal(str(feature)) for feature in
                      self._binary_features_model.base_features])
        feature_value = Group((plus ^ minus ^ homorganic_variable) + feature)
        feature_set = Suppress(open_marker) + ZeroOrMore(feature_value) + \
            Suppress(close_marker)
        #feature_set.setParseAction(self._handle_base_feature_set)
        return feature_set
        
    def _define_cluster (self):
        """Returns a `pyparsing.ParserElement` representing an IPA
        cluster."""
        base_characters = ''.join([str(character) for character in
                                   self._binary_features_model.base_characters])
        diacritic_characters = ''.join([str(character) for character in
                                        self._binary_features_model.diacritic_characters])
        spacing_characters = ''.join([str(character) for character in
                                      self._binary_features_model.spacing_characters])
        suprasegmental_characters = ''.join([str(character) for character in
                                             self._binary_features_model.suprasegmental_characters])
        base_character = Word(base_characters, exact=1)
        diacritic_character = Word(diacritic_characters, exact=1)
        spacing_character = Word(spacing_characters, exact=1)
        suprasegmental_character = Word(suprasegmental_characters, exact=1)
        phoneme = Combine(base_character + ZeroOrMore(diacritic_character) +
                          ZeroOrMore(spacing_character))
        cluster = phoneme ^ OneOrMore(suprasegmental_character)
        cluster.setParseAction(self._handle_cluster)
        return cluster

    def _define_context_component (self, cluster, base_feature_set):
        placeholder = Literal(SOURCE_PLACEHOLDER)
        placeholder.setParseAction(self._handle_placeholder)
        context_component = Group(ZeroOrMore(cluster ^ base_feature_set) + \
            placeholder + ZeroOrMore(cluster ^ base_feature_set)).setResultsName('context_component')
        context_component.setParseAction(self._handle_context_component)
        return context_component
    
    def _define_grammar (self):
        heading_open = Literal('[').suppress()
        heading_close = Literal(']').suppress()
        cluster = self._define_cluster()
        base_feature_set = self._define_base_feature_set()
        rule = self._define_rule(cluster, base_feature_set)
        rules = OneOrMore(rule).setResultsName('rules')
        date_number = Word('-'+nums, nums).setResultsName('date_number')
        date_number.setParseAction(self._handle_date_number)
        date_name = Combine(OneOrMore(Word(alphanums+'.')), adjacent=False,
                            joinString=' ').setResultsName('date_name')
        date_heading = heading_open + Suppress(Keyword('Date')) + date_number \
            + date_name + heading_close
        date_section = date_heading + rules
        date_sections = Group(OneOrMore(date_section))
        language_name = Combine(OneOrMore(Word(alphas)), adjacent=False,
                                joinString=' ').setResultsName('language_name')
        language_heading = heading_open + Suppress(Keyword('Language')) + \
            language_name + heading_close
        language_section = Group(language_heading + date_sections)
        ruleset = OneOrMore(language_section)
        return ruleset

    def _define_result_component (self, cluster, base_feature_set):
        result_component = Group(ZeroOrMore(cluster ^ base_feature_set)).setResultsName('result_component')
        result_component.setParseAction(self._handle_result_component)
        return result_component
    
    def _define_rule (self, cluster, base_feature_set):
        source_component = self._define_source_component(
            cluster, base_feature_set)
        result_component = self._define_result_component(
            cluster, base_feature_set)
        context_component = self._define_context_component(
            cluster, base_feature_set)
        component_divider = Literal(RULE_COMPONENT_DIVIDER).suppress()
        rule = Group(Suppress('Rule') + source_component + component_divider + \
            result_component + component_divider + context_component)
        return rule

    def _define_source_component (self, cluster, base_feature_set):
        source_component = Group(ZeroOrMore(cluster ^ base_feature_set)).setResultsName('source_component')
        source_component.setParseAction(self._handle_source_component)
        return source_component

    def _handle_cluster (self, string, location, tokens):
        base = BaseCharacter(self._binary_features_model, tokens[0])
        cluster = BaseCluster(self._binary_features_model,
                              base_character=base)
        self._current_rule_component.append(cluster)

    def _handle_context_component (self, string, location, tokens):
        context_component = self._current_rule_component
        self._current_rule_component = SourceRuleComponent()
        return context_component        

    def _handle_date_number (self, string, location, tokens):
        return int(tokens[0])

    def _handle_placeholder (self, string, location, tokens):
        placeholder = Placeholder(self._binary_features_model,
                                  self._current_source_component)
        self._current_rule_component.append(placeholder)

    def _handle_result_component (self, string, location, tokens):
        result_component = self._current_rule_component
        self._current_rule_component = ContextRuleComponent()
        return result_component
        
    def _handle_source_component (self, string, location, tokens):
        source_component = self._current_rule_component
        self._current_rule_component = ResultRuleComponent()
        self._current_source_component = source_component
        return source_component

    def parse (self, configuration):
        """Parses `configuration` and returns a `.Ruleset` generated
        from it.

        :param configuration: ruleset configuration
        :type configuration: `str`
        :rtype: `.Ruleset`

        """
        data = self._grammar.parseString(configuration)
        return self._create_ruleset(data)
