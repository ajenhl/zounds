from .suprasegmental_feature import SuprasegmentalFeature
from .character import Character
from .constants import SNFM


class SuprasegmentalCharacter (Character):

    _feature_type = SuprasegmentalFeature
    _normalised_form_marker = SNFM

    def __new__ (cls, binary_features_model, ipa):
        return Character._create_new(cls, binary_features_model, ipa)
