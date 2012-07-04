from .base_feature import BaseFeature
from .constants import HAS_FEATURE, NOT_HAS_FEATURE
from .character import Character


class BaseCharacter (Character):

    _feature_type = BaseFeature
    _valid_feature_values = (HAS_FEATURE, NOT_HAS_FEATURE)

    def __new__ (cls, binary_features_model, ipa):
        return Character._create_new(cls, binary_features_model, ipa)
