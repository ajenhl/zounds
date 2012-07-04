from .base_feature import BaseFeature
from .character import Character


class SpacingCharacter (Character):

    _feature_type = BaseFeature

    def __new__ (cls, binary_features_model, ipa):
        return Character._create_new(cls, binary_features_model, ipa)

