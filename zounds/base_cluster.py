from .base_character import BaseCharacter
from .cluster import Cluster, Counter
from .diacritic_character import DiacriticCharacter
from .exceptions import IllegalArgumentError, MismatchedModelsError, MismatchedTypesError, NormalisedFormValueError
from .spacing_character import SpacingCharacter


class BaseCluster (Cluster):

    def __init__ (self, binary_features_model, base_character=None,
                  diacritic_characters=None, spacing_characters=None,
                  normalised_form=None):
        """Initialise this object.

        It is an error to supply both `normalised_form` and any other
        argument. If `normalised_form` is not supplied,
        `base_character` must be supplied.
        
        While a `.BaseCluster` may be created directly with a
        `.NormalisedForm`, it is better to create a `.Cluster` with a
        `.NormalisedForm`; it will return either a `.BaseCluster` or
        `.SuprasegmentalCluster` as appropriate.

        :param binary_features_model: the binary features model for this cluster
        :type binary_features_model: `.BinaryFeaturesModel`
        :param base_character: the base character in the cluster
        :type base_character: `.BaseCharacter`
        :param diacritic_characters: diacritic characters in the cluster
        :type diacritic_characters: `list` of `.DiacriticCharacter`\s
        :param spacing_characters: spacing characters in the cluster
        :type spacing_characters: `list` of `.SpacingCharacter`\s
        :param normalised_form: the normalised form of the cluster
        :type normalised_form: `.BaseNormalisedForm`

        """
        super().__init__(binary_features_model)
        if not base_character and not normalised_form:
            # QAZ: error message.
            raise IllegalArgumentError()
        if normalised_form and (base_character or diacritic_characters
                                or spacing_characters):
            # QAZ: error message.
            raise IllegalArgumentError()
        diacritic_characters = diacritic_characters or []
        spacing_characters = spacing_characters or []
        self._base_character = base_character
        self._diacritic_characters = diacritic_characters
        self._spacing_characters = spacing_characters
        self._normalised_form = normalised_form
        if base_character:
            self._test_matching_types(base_character, BaseCharacter)
            self._test_matching_models(base_character,
                                       self._binary_features_model)
            for character in diacritic_characters:
                self._test_matching_types(character, DiacriticCharacter)
                self._test_matching_models(character,
                                           self._binary_features_model)
            for character in spacing_characters:
                self._test_matching_types(character, SpacingCharacter)
                self._test_matching_models(character,
                                           self._binary_features_model)
        else:
            self._resolve_normalised_form()

    def __new__ (cls, *args, **kwargs):
        return object.__new__(cls)

    def __str__ (self):
        diacritics = ''.join([str(character) for character in
                              self.diacritic_characters])
        spacing = ''.join([str(character) for character in
                           self.spacing_characters])
        return '{}{}{}'.format(self.base_character, diacritics, spacing)

    @property
    def base_character (self):
        """Returns the base character in this cluster.

        :rtype: `.BaseCharacter`

        """
        return self._base_character

    @property
    def diacritic_characters (self):
        """Returns a list of diacritic characters in this cluster.

        :rtype: `list` of :py:class:`.DiacriticCharacter`\s

        """
        return self._diacritic_characters

    def _get_matching_characters (self, normalised_form):
        """Returns a list of characters that match some or all of the
        feature values in `normalised_form`.

        The list is sorted in descending order of how many feature
        values each character matches.

        :param normalised_form: normalised form to analyse
        :type normalised_form: `.NormalisedForm`
        :rtype: `list` of `.Character`\s

        """
        index = 0
        counter = Counter()
        for feature_value in normalised_form:
            feature = self._binary_features_model.base_features[index]
            for character in feature.get_value_characters(feature_value):
                counter.add(character)
            index += 1
        return counter.get_sorted()

    @property
    def normalised_form (self):
        """Returns the normalised form of this cluster.

        :rtype: `.BaseNormalisedForm`

        """
        if not self._normalised_form:
            normalised_form = self._base_character.normalised_form
            for diacritic_character in self._diacritic_characters:
                normalised_form += diacritic_character.normalised_form
            for spacing_character in self._spacing_characters:
                normalised_form += spacing_character.normalised_form
            self._normalised_form = normalised_form
        return self._normalised_form

    def _resolve_normalised_form (self):
        """Resolves this cluster's normalised form into a base
        character, diacritic and spacing characters.

        Resolution has one arbitrary rule, that no modifier character
        (diacritic or spacing character) specify a feature value
        (HAS_FEATURE or NOT_HAS_FEATURE) that the base character has
        already correctly set.
        
        """
        characters = self._get_matching_characters(self.normalised_form)
        for character in characters:
            self._base_character = character
            # Determine the normalised form of the remaining required
            # characters.
            required_normalised_form = self.normalised_form - \
                character.normalised_form
            # If no specific feature values are required, the current
            # character is the sole required character.
            if required_normalised_form.is_empty():
                break
            # Otherwise, diacritics and/or spacing characters are
            # required, so find ones that match. Clear the diacritic
            # and spacing characters that may have resulted from
            # previous attempts with a different base character.
            self._diacritic_characters = []
            self._spacing_characters = []
            # If modifiers have satisfied the required normalised
            # form, the normalised form has been fully
            # resolved. Otherwise, try the next best fitting
            # character.
            if self._set_modifiers(required_normalised_form):
                break
        else:
            # No set of characters has matched.
            # QAZ: error message and proper exception.
            raise Exception('No set of characters could be found to resolve this cluster\'s normalised form')

    def _set_modifiers (self, required_normalised_form):
        """Returns True if modifier characters sufficient to produce
        `required_normalised_form` are set.

        :param required_normalised_form: the normalised form that must
          be produced
        :type required_normalised_form: `.BaseNormalisedForm`
        :rtype: `bool`

        """        
        modifier_characters = self._get_matching_characters(
            required_normalised_form)
        for modifier_character in modifier_characters:
            if isinstance(modifier_character, BaseCharacter):
                continue
            try:
                required_normalised_form = required_normalised_form - \
                    modifier_character.normalised_form
            except NormalisedFormValueError:
                # Some characters will specify HAS_FEATURE or
                # NOT_HAS_FEATURE for features that the base character
                # has already set to the required value. These are not
                # considered.
                continue
            if isinstance(modifier_character, DiacriticCharacter):
                self._diacritic_characters.append(modifier_character)
            else:
                self._spacing_characters.append(modifier_character)
            if required_normalised_form.is_empty():
                return True
        return False

    @property
    def spacing_characters (self):
        """Returns a list of the spacing characters in this cluster.

        :rtype: `list` of `.SpacingCharacter`\s

        """
        return self._spacing_characters
    
    @staticmethod
    def _test_matching_models (character, binary_features_model):
        """Raises `.MismatchedModelsError` if `character`'s binary
        features model does not match `binary_features_model`.

        :param character: character to test
        :type character: `.Character`
        :param binary_features_model: binary features model
        :type binary_features_model: `.BinaryFeaturesModel`

        """
        if character.binary_features_model != binary_features_model:
            # QAZ: error message.
            raise MismatchedModelsError()

    @staticmethod
    def _test_matching_types (character, cls):
        """Raises `.MismatchedTypesError` if `character` is not an
        instance of `cls`.

        :param character: character to test
        :type character: `.Character`
        :param cls: class to test character against
        :type cls: `type`

        """
        if not isinstance(character, cls):
            # QAZ: error message.
            raise MismatchedTypesError()
