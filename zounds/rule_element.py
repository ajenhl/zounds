class RuleElement:

    """Base class for all elements that can occur within a rule."""

    def __init__ (self, binary_features_model):
        self._binary_features_model = binary_features_model
    
    @property
    def applier_form (self):
        """Returns this element in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        raise NotImplementedError

    @property
    def binary_features_model (self):
        """Returns the `.BinaryFeaturesModel` associated with this
        element.

        :rtype: `.BinaryFeaturesModel`

        """
        return self._binary_features_model
