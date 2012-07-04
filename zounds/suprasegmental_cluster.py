from .cluster import Cluster
from .exceptions import IllegalArgumentError, MismatchedModelsError, MismatchedTypesError
from .suprasegmental_character import SuprasegmentalCharacter


class SuprasegmentalCluster (Cluster):

    def __init__ (self, binary_features_model, suprasegmental_characters=None,
                  normalised_form=None):
        super().__init__(binary_features_model)
        if not suprasegmental_characters and not normalised_form:
            # QAZ: error message.
            raise IllegalArgumentError()
        if suprasegmental_characters and normalised_form:
            # QAZ: error message.
            raise IllegalArgumentError()
        self._normalised_form = normalised_form
        self._suprasegmental_characters = suprasegmental_characters or []
        for character in self._suprasegmental_characters:
            if not isinstance(character, SuprasegmentalCharacter):
                # QAZ: error message.
                raise MismatchedTypesError()
            if character.binary_features_model != self._binary_features_model:
                # QAZ: error message.
                raise MismatchedModelsError()

    def __new__ (cls, *args, **kwargs):
        return object.__new__(cls)

    def __str__ (self):
        return ''.join([str(character) for character in
                       self._suprasegmental_characters])

    @property
    def normalised_form (self):
        """Returns the normalised form of this cluster.

        :rtype: `.SuprasegmentalNormalisedForm`

        """
        if not self._normalised_form:
            normalised_form = self._suprasegmental_characters[0].normalised_form
            for character in self._suprasegmental_characters[1:]:
                normalised_form += character.normalised_form
            self._normalised_form = normalised_form
        return self._normalised_form
