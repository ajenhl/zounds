from .constants import HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from .base_character import BaseCharacter
from .base_feature import BaseFeature
from .diacritic_character import DiacriticCharacter
from .exceptions import InvalidCharacterError, MismatchedModelsError, MismatchedTypesError
from .spacing_character import SpacingCharacter
from .suprasegmental_character import SuprasegmentalCharacter
from .suprasegmental_feature import SuprasegmentalFeature


class BinaryFeaturesModel:

    def __init__ (self):
        # A dictionary mapping characters to base feature values. The
        # keys of this dictionary are `Character`s and the values are
        # themselves dictionaries. The keys of the sub-dictionaries
        # are `Feature`s, and each value is the value (HAS_FEATURE,
        # INAPPLICABLE_FEATURE or NOT_HAS_FEATURE) a character has for
        # that feature.
        self._character_values = {}
        # A dictionary mapping features to characters. The keys of
        # this dictionary are `Feature`s and the values are themselves
        # dictionaries. The keys of the sub-dictionaries are the
        # possible feature values (HAS_FEATURE, INAPPLICABLE_FEATURE
        # and NOT_HAS_FEATURE), and each value is a set of
        # `Character`s that have that value for that feature.
        self._feature_values = {}

    def _add_character (self, character):
        """Adds `character` to this model.

        :param character: character to add
        :type character: `.Character`

        """
        self._character_values[character] = {}

    def _add_feature (self, feature):
        """Adds `feature` to this model.

        :param feature: feature to add
        :type feature: `.Feature`

        """
        self._feature_values[feature] = {
            HAS_FEATURE: set(), NOT_HAS_FEATURE: set(),
            INAPPLICABLE_FEATURE: set()}

    @property
    def base_characters (self):
        """Returns a `list` of `.BaseCharacter` in this model.

        :rtype: `list` of `.BaseCharacter`\s

        """
        return [character for character in self._character_values.keys()
                if isinstance(character, BaseCharacter)]

    @property
    def base_features (self):
        """Returns a `list` of `.BaseFeature`\s in this model.

        The list is sorted alphabetically by feature name.
        
        :rtype: `list` of `.BaseFeature`\s

        """
        features = [feature for feature in self._feature_values.keys()
                    if isinstance(feature, BaseFeature)]
        features.sort()
        return features

    @property
    def diacritic_characters (self):
        """Returns a `list` of `.DiacriticCharacter` in this model.

        :rtype: `list` of `.DiacriticCharacter`\s

        """
        return [character for character in self._character_values.keys()
                if isinstance(character, DiacriticCharacter)]
    
    def get_character_feature_value (self, character, feature):
        """Returns the value `character` has for `feature`.

        :param character: the character having the value
        :type character: `.Character`
        :param feature: the feature
        :type feature: `.Feature`
        :rtype: `str`

        """
        self._test_matching_models(character, feature)
        self._test_matching_types(character, feature)
        return self._get_character_feature_value(character, feature)

    def _get_character_feature_value (self, character, feature):
        """Returns the value `character` has for `feature`.

        This method performs the actual lookup, without checking for
        matching models or types.

        :param character: the character having the value
        :type character: `.Character`
        :param feature: the feature
        :type feature: `.Feature`
        :rtype: `str`

        """
        try:
            return self._character_values[character][feature]
        except KeyError:
            raise InvalidCharacterError(
                'Character {} has no value defined for feature {}'.format(
                    character, feature))
    
    def get_character_feature_values (self, character):
        """Returns a `list` of all feature values for `character`.

        The list is sorted alphabetically by feature name.

        :param character: the character
        :type character: `.Character`
        :rtype: `list` of `str`

        """
        feature_values = []
        if isinstance(character, SuprasegmentalCharacter):
            features = self.suprasegmental_features
        else:
            features = self.base_features
        for feature in features:
            feature_value = self._get_character_feature_value(
                character, feature)
            feature_values.append(feature_value)
        return feature_values

    def get_feature_value_characters (self, feature, value):
        """Returns the `set` of `.Character`\s that have `value` for
        `feature`.

        :param feature: the feature
        :type feature: `.Feature`
        :param value: feature value
        :type value: `str`
        :rtype: `set` of `.Character`\s

        """
        return self._feature_values[feature][value]
    
    def _remove_character (self, character):
        """Removes `character` from this model.

        :param character: character to remove
        :type character: `.Character`
        
        """
        del self._character_values[character]
        for value_dict in self._feature_values.values():
            for character_set in value_dict.values():
                character_set.discard(character)

    def _remove_feature (self, feature):
        """Removes `feature` from this model.

        :param feature: feature to remove
        :type feature: `.Feature`

        """
        del self._feature_values[feature]
        for feature_dict in self._character_values.values():
            try:
                del feature_dict[feature]
            except KeyError:
                # The feature may be deleted before a character has
                # set a value for it. This is not an error.
                pass

    def set_character_feature_value (self, character, feature, value):
        """Sets the value `character` has for `feature`.

        :param character: the character whose feature value is being set
        :type character: `.Character`
        :param feature: the feature whose value is being set
        :type feature: `.Feature`
        :param value: the value to be set
        :type value: `str`

        """
        self._test_matching_models(character, feature)
        self._test_matching_types(character, feature)
        try:
            existing_value = self._get_character_feature_value(
                character, feature)
            if existing_value == value:
                return
            self._feature_values[feature][existing_value].discard(character)
        except InvalidCharacterError:
            pass
        self._feature_values[feature][value].add(character)
        self._character_values[character][feature] = value
            
    @property
    def spacing_characters (self):
        """Returns a `list` of `.SpacingCharacter`\s in this model.

        :rtype: `list` of `.SpacingCharacter`\s

        """
        return [character for character in self._character_values.keys()
                if isinstance(character, SpacingCharacter)]

    @property
    def suprasegmental_characters (self):
        """Returns a `list` of `.SuprasegmentalCharacter`\s in this
        model.

        :rtype: `list` of `.SuprasegmentalCharacter`\s

        """
        return [character for character in self._character_values.keys()
                if isinstance(character, SuprasegmentalCharacter)]

    @property
    def suprasegmental_features (self):
        """Returns a `list` of `.SuprasegmentalFeature`\s in this
        model.

        The list is sorted alphabetically by feature name.

        :rtype: `list` of `.SuprasegmentalFeature`\s

        """
        features = [feature for feature in self._feature_values.keys()
                    if isinstance(feature, SuprasegmentalFeature)]
        features.sort()
        return features

    @staticmethod
    def _test_matching_models (character, feature):
        """Raises a `.MismatchedModelError` if the
        `BinaryFeaturesModel` for this `.Character` does not match that
        of `feature`.

        :param character: character to check
        :type character: `.Character`
        :param feature: the feature to be tested against
        :type feature: `.Feature`

        """
        if feature.binary_features_model != character.binary_features_model:
            # QAZ: error message.
            raise MismatchedModelsError()

    @staticmethod
    def _test_matching_types (character, feature):
        """Raises a `.MismatchedTypesError` if the subclass of
        `character` is not associated with the subclass of `feature`.

        :param character: character to check
        :type character: `.Character`
        :param feature: the feature to be tested against
        :type feature: `.Feature`

        """
        if character.feature_type != feature.__class__:
            # QAZ: error message.
            raise MismatchedTypesError()
