from .constants import BNFM, HAS_FEATURE, INAPPLICABLE_FEATURE, NOT_HAS_FEATURE
from .exceptions import IllegalArgumentError, InvalidCharacterError
from .normalised_form import NormalisedForm
from .word_element import WordElement


class Character (WordElement):

    _cache = {}
    _normalised_form_marker = BNFM
    _valid_feature_values = (HAS_FEATURE, INAPPLICABLE_FEATURE,
                             NOT_HAS_FEATURE)

    def __init__ (self, binary_features_model, ipa):
        """Initialises a new `.Character` object.

        :param binary_features_model: the `.BinaryFeaturesModel` that
          this `.Character` is associated with
        :type binary_features_model: `.BinaryFeaturesModel`
        :param ipa: IPA character that this `.Character` represents
        :type ipa: str

        """
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.binary_features_model = binary_features_model
            self._ipa = ipa
            self.binary_features_model._add_character(self)

    def __str__ (self):
        return self.ipa

    @staticmethod
    def _create_new (cls, binary_features_model, ipa):
        # Cache instances by their initialisation arguments.
        if len(ipa) != 1:
            raise InvalidCharacterError(
                'The IPA form of a character must be a single character')
        try:
            existing = Character._cache[(binary_features_model, ipa)]
        except KeyError:
            obj = object.__new__(cls)
            Character._cache[(binary_features_model, ipa)] = obj
            return obj
        if not isinstance(existing, cls):
            raise InvalidCharacterError(
                'Character for this IPA form exists but is of a different type')
        return existing

    def delete (self):
        """Deletes this character, removing it from the
        `.BinaryFeaturesModel`."""
        self.binary_features_model._remove_character(self)
        del Character._cache[(self.binary_features_model, self.ipa)]
        self.binary_features_model = None

    @property
    def feature_type (self):
        """Returns the specific type of feature that may be associated
        with this character.

        :rtype: `type`

        """
        return self._feature_type

    def get_feature_value (self, feature):
        """Returns the value this character has for `feature`.

        Raises `.InvalidCharacterError` if the value is not in the list
        of valid feature values for this type of character.

        :param feature: the feature whose value for this character is
          to be returned
        :type feature: `.Feature`
        :rtype: `str`

        """
        value = self.binary_features_model.get_character_feature_value(
            self, feature)
        return value

    @property
    def ipa (self):
        """Returns the IPA form of this character.

        :rtype: `str`

        """
        return self._ipa

    @ipa.setter
    def ipa (self, ipa):
        """Sets the IPA form of this character to `ipa`.

        :param ipa: IPA character to set
        :type ipa: `str`

        """
        if ipa == self.ipa:
            return
        if len(ipa) != 1:
            raise InvalidCharacterError(
                'The IPA form of a character must be a single character')
        if (self.binary_features_model, ipa) in Character._cache:
            raise InvalidCharacterError(
                'A character with that IPA form already exists')
        Character._cache[(self.binary_features_model, ipa)] = self
        del Character._cache[(self.binary_features_model, self.ipa)]
        self._ipa = ipa

    @property
    def normalised_form (self):
        """Returns the normalised form of this character.

        :rtype: `.NormalisedForm`

        """
        feature_values = self.binary_features_model.get_character_feature_values(self)
        return NormalisedForm(self._normalised_form_marker +
                              ''.join(feature_values))

    def set_feature_value (self, feature, value):
        """Sets the value this character for `feature`.

        Raises `.IllegalArgumentError` if `value` is not in the list of
        valid feature values for this type of character.
        
        :param feature: the feature whose value for this character is
          to be returned
        :type feature: `.Feature`
        :param value: the value to set
        :type value: `str`

        """
        if value not in self._valid_feature_values:
            # QAZ: error message.
            raise IllegalArgumentError()
        self.binary_features_model.set_character_feature_value(
            self, feature, value)

