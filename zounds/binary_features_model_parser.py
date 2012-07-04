from pyparsing import alphas, delimitedList, Dict, Group, Literal, OneOrMore, Optional, ParseException, ParseFatalException, StringEnd, Suppress, Word

from .base_character import BaseCharacter
from .base_feature import BaseFeature
from .binary_features_model import BinaryFeaturesModel
from .constants import BASE_CHARACTERS, DIACRITIC_CHARACTERS, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE, SPACING_CHARACTERS, SUPRASEGMENTAL_CHARACTERS
from .diacritic_character import DiacriticCharacter
from .spacing_character import SpacingCharacter
from .suprasegmental_character import SuprasegmentalCharacter
from .suprasegmental_feature import SuprasegmentalFeature


class BinaryFeaturesModelParser:

    """Class for parsing a binary features model configuration and
    generating a `.BinaryFeaturesModel` object."""

    def __init__ (self):
        self._grammar = self._define_grammar()

    def _create_characters (self, model, feature_names, data, character_type,
                            feature_type):
        """Creates characters and sets their feature values from `data`.

        :param model: binary features model being created
        :type model: `.BinaryFeaturesModel`
        :param feature_names: all defined feature names of `feature_type`
        :type feature_names: `list` of `str`
        :param data: character and feature value data
        :type data: `dict` with `list` values
        :param character_type: type of characters to create
        :type character_type: `type`
        :param feature_type: type of features to use
        :type feature_type: `type`

        """
        for symbol, feature_values in data:
            remaining_feature_names = feature_names[:]
            character = character_type(model, symbol)
            for feature_value, feature_name in feature_values:
                feature = feature_type(model, feature_name)
                character.set_feature_value(feature, feature_value)
                remaining_feature_names.remove(feature_name)
            for feature_name in remaining_feature_names:
                feature = feature_type(model, feature_name)
                character.set_feature_value(feature, INAPPLICABLE_FEATURE)

    def _create_model (self, data):
        """Returns a new `.BinaryFeaturesModel` generated using `data`.

        :param data: output data from the parsing
        :type data: `dict`
        :rtype: `.BinaryFeaturesModel`
        
        """
        model = BinaryFeaturesModel()
        # Create base features.
        for feature_name in data['base_features']:
            BaseFeature(model, feature_name)
        # Create and set feature values for base characters. Only
        # HAS_FEATURE features are specified, so fill in the
        # NOT_HAS_FEATURE by inference.
        for character_data in data['base_characters']:
            symbol = character_data[0]
            character = BaseCharacter(model, symbol)
            feature_names = character_data[1:]
            for feature_name in data['base_features']:
                if feature_name in feature_names:
                    feature_value = HAS_FEATURE
                else:
                    feature_value = NOT_HAS_FEATURE
                feature = BaseFeature(model, feature_name)
                character.set_feature_value(feature, feature_value)
        # Create and set feature values for diacritic characters.
        diacritic_characters = data.get('diacritic_characters', None)
        if diacritic_characters is not None:
            self._create_characters(model, data['base_features'],
                                    diacritic_characters,
                                    DiacriticCharacter, BaseFeature)
        # Create and set feature values for spacing characters.
        spacing_characters = data.get('spacing_characters', None)
        if spacing_characters is not None:
            self._create_characters(model, data['base_features'],
                                    spacing_characters,
                                    SpacingCharacter, BaseFeature)
        # Create suprasegmental features.
        suprasegmental_features = data.get('suprasegmental_features', None)
        if suprasegmental_features is not None:
            for feature_name in suprasegmental_features:
                SuprasegmentalFeature(model, feature_name)
            # Create and set feature values for suprasegmental characters.
                self._create_characters(model, suprasegmental_features,
                                        data['suprasegmental_characters'],
                                        SuprasegmentalCharacter,
                                        SuprasegmentalFeature)
        return model

    def _define_base_characters_section (self):
        heading = Literal('[Base Characters]')
        character = Word(''.join(BASE_CHARACTERS), exact=1).setResultsName(
            'character')
        character.setParseAction(self._handle_character)
        feature = Word(alphas).setResultsName('feature')
        feature.setParseAction(self._handle_character_base_feature)
        features = delimitedList(feature)
        character_definition = Group(character + Suppress(':') + \
                                         Optional(features))
        character_definitions = Group(OneOrMore(character_definition)).setResultsName('base_characters')
        section = Suppress(heading) + character_definitions
        return section
        
    def _define_base_features_section (self):
        return self._define_features_section('Base Features', 'base_features',
                                             self._handle_base_feature)

    def _define_diacritic_characters_section (self):
        # Remove the initial space in each item in the list of
        # diacritic characters.
        characters = [item[1] for item in DIACRITIC_CHARACTERS]
        return self._define_valued_characters_section(
            'Diacritic Characters', characters,
            self._handle_character_base_feature, 'diacritic_characters')

    def _define_features_section (self, heading, name, parse_action):
        """Returns a parser object for a feature section.

        :param heading: section heading
        :type heading: `str`
        :param name: name for results
        :type name: `str`
        :param parse_action: parse action for a feature
        :type parse_action: `function`

        """
        heading = Literal('[{}]'.format(heading))
        feature = Word(alphas).setResultsName('feature')
        feature.setParseAction(parse_action)
        features = Group(OneOrMore(feature)).setResultsName(name)
        section = Suppress(heading) + features
        return section
    
    def _define_grammar (self):
        base_features_section = self._define_base_features_section()
        base_characters_section = self._define_base_characters_section()
        diacritic_characters_section = self._define_diacritic_characters_section()
        spacing_characters_section = self._define_spacing_characters_section()
        suprasegmental_features_section = self._define_suprasegmental_features_section()
        suprasegmental_characters_section = self._define_suprasegmental_characters_section()
        binary_features_model = base_features_section + \
            base_characters_section + \
            Optional(diacritic_characters_section) + \
            Optional(spacing_characters_section) + \
            Optional(suprasegmental_features_section + \
            suprasegmental_characters_section) + StringEnd()
        return binary_features_model

    def _define_spacing_characters_section (self):
        return self._define_valued_characters_section(
            'Spacing Characters', SPACING_CHARACTERS,
            self._handle_character_base_feature, 'spacing_characters')

    def _define_suprasegmental_characters_section (self):
        return self._define_valued_characters_section(
            'Suprasegmental Characters', SUPRASEGMENTAL_CHARACTERS,
            self._handle_character_suprasegmental_feature,
            'suprasegmental_characters')

    def _define_suprasegmental_features_section (self):
        return self._define_features_section(
            'Suprasegmental Features', 'suprasegmental_features',
            self._handle_suprasegmental_feature)
    
    def _define_valued_characters_section(self, heading, characters,
                                          parse_action, character_type):
        """Returns a parser object for a section specifying characters
        and their valued features.

        :param heading: section heading
        :type heading: `str`
        :param characters: valid characters
        :type characters: `list` of `str`
        :param parse_action: parse action for a character
        :type parse_action: `function`
        :param character_type: type of characters being described
        :type character_type: `str`

        """
        heading = Literal('[{}]'.format(heading))
        character = Word(''.join(characters), exact=1).setResultsName(
            'character')
        character.setParseAction(self._handle_character)
        feature = Word(alphas).setResultsName('feature')
        feature.setParseAction(parse_action)
        value = Literal('+') ^ Literal('-') ^ Literal('\N{MINUS SIGN}')
        value.setParseAction(self._handle_feature_value)
        feature_value = Group(value + feature)
        feature_values = Group(delimitedList(feature_value))
        character_definition = Dict(Group(character + Suppress(':') +
                                          feature_values))
        character_definitions = Group(OneOrMore(character_definition)).setResultsName(character_type)
        section = Suppress(heading) + character_definitions
        return section

    def _handle_base_feature (self, string, location, tokens):
        return self._handle_feature(string, location, tokens,
                                    self._base_features)

    def _handle_character (self, string, location, tokens):
        character = tokens['character']
        if character in self._characters:
            message = 'Character "{}" is already defined'.format(character)
            raise ParseFatalException(string, location, message)
        self._characters.append(character)
        
    def _handle_character_base_feature (self, string, location, tokens):
        features = self._base_features
        return self._handle_character_feature(string, location, tokens,
                                              features)

    def _handle_character_feature (self, string, location, tokens, features):
        feature = tokens['feature']
        if feature not in features:
            message = '"{}" is not a defined feature'.format(feature)
            # Raise a ParseException rather than a ParseFatalException
            # because the parser may backtrack from an empty base
            # character definition to the next base character
            # definition.
            raise ParseException(string, location, message)

    def _handle_character_suprasegmental_feature (self, string, location,
                                                  tokens):
        features = self._suprasegmental_features
        return self._handle_character_feature(string, location, tokens,
                                              features)

    def _handle_feature (self, string, location, tokens, features):
        feature = tokens['feature']
        # Always check base features, since a suprasegmental feature
        # may not have the same name as a base feature.
        if feature in features or feature in self._base_features:
            message = 'Feature name "{}" is duplicated'.format(feature)
            raise ParseFatalException(string, location, message)
        features.append(feature)

    def _handle_feature_value (self, string, location, tokens):
        value = tokens[0]
        if value == '+':
            tokens[0] = HAS_FEATURE
        else:
            tokens[0] = NOT_HAS_FEATURE
        return tokens
        
    def _handle_suprasegmental_feature (self, string, location, tokens):
        return self._handle_feature(string, location, tokens,
                                    self._suprasegmental_features)
    
    def parse (self, definition):
        """Returns a `.BinaryFeaturesModel` parsed from `definition`.

        :param definition: binary features model definition
        :type definition: `str`
        :rtype: `.BinaryFeaturesModel`

        """
        self._base_features = []
        self._suprasegmental_features = []
        self._characters = []
        data = self._grammar.parseString(definition)
        binary_features_model = self._create_model(data)
        return binary_features_model
