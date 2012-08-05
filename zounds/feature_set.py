from .constants import AFM, INAPPLICABLE_FEATURE
from .exceptions import MismatchedTypesError
from .normalised_form import NormalisedForm
from .rule_element import RuleElement
from .word_element import WordElement


class FeatureSet (RuleElement, WordElement):

    def __init__ (self, binary_features_model):
        super().__init__(binary_features_model)
        self._features = getattr(binary_features_model,
                                 self._feature_type_property)
        # Dictionary mapping feature values to features.
        self._feature_values = {}

    @property
    def applier_form (self):
        """Returns this feature set in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        return '{}{}'.format(AFM, self.normalised_form)

    @property
    def normalised_form (self):
        """Returns the normalised form of this feature set.

        :rtype: `.NormalisedForm`

        """
        values = []
        for feature in self._features:
            value = self._feature_values.get(feature, INAPPLICABLE_FEATURE)
            values.append(value)
        return NormalisedForm(self._normalised_form_marker +
                              ''.join(values))
        
    def set (self, feature, feature_value):
        """Sets `feature` to `feature_value` in this feature set.

        `feature_value` may be HAS_FEATURE, NOT_HAS_FEATURE, a
        homorganic variable, or None (which clears the feature from
        the feature set).

        :param feature: feature whose value is to be set
        :type feature: `.Feature`
        :param feature_value: feature value to set
        :type feature_value: `str` or None

        """
        if feature not in self._features:
            # QAZ: error message.
            raise MismatchedTypesError()
        if feature_value is None:
            # It is of no consequence if the feature has no existing
            # value when it is being removed anyway.
            self._feature_values.pop(feature, None)
        else:
            self._feature_values[feature] = feature_value
