class IllegalArgumentError (Exception):

    """Exception raised when a function or method argument's value is
    invalid."""

    pass


class InvalidCharacterError (Exception):

    """Exception raised when an operation is performed on a
    `.Character` that is invalid, or when an operation will make a
    `.Character` invalid."""

    pass


class InvalidFeatureError (Exception):
    """Exception raised when an operation is performed on a
    `.Feature` that is invalid, or when an operation will make a
    `.Feature` invalid."""

    pass


class InvalidRuleError (Exception):
    """Exception raised when an operation is performed on a `.Rule`
    that is invalid."""

    pass


class MismatchedModelsError (Exception):

    """Exception raised when an object associated with one
    `.BinaryFeaturesModel` is used in conjunction with an object
    associated with another `.BinaryFeaturesModel`."""
    
    pass


class MismatchedTypesError (Exception):

    """Exception raised whenever objects of incompatible types are
    used together. For example, a `.BaseFeature` with a
    `.SuprasegmentalCharacter`."""

    pass


class NormalisedFormValueError (Exception):

    """Exception raised when a normalised form has an invalid value,
    as when two normalised forms of different lengths are added."""

    pass
