from .feature import Feature


class SuprasegmentalFeature (Feature):

    def __new__ (cls, binary_features_model, name):
        return Feature._create_new(cls, binary_features_model, name)
