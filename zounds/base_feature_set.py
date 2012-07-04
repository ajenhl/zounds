from .constants import BNFM
from .feature_set import FeatureSet


class BaseFeatureSet (FeatureSet):

    _feature_type_property = 'base_features'
    _normalised_form_marker = BNFM
