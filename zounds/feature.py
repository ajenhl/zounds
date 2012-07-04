from .exceptions import InvalidFeatureError


class Feature:

    _cache = {}

    def __init__ (self, binary_features_model, name):
        """Initialises a new `.Feature` object.

        :param binary_features_model: the `.BinaryFeaturesModel` that
          this `.Feature` is associated with
        :type binary_features_model: `.BinaryFeaturesModel`
        :param name: the name of this `.Feature`
        :type name: string

        """
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.binary_features_model = binary_features_model
            self._name = name
            self.binary_features_model._add_feature(self)

    def __lt__ (self, other):
        # For sorting purposes.
        return self.name < other.name

    def __str__ (self):
        return self.name
    
    @staticmethod
    def _create_new (cls, binary_features_model, name):
        # Cache instances by their initialisation arguments.
        try:
            existing = Feature._cache[(binary_features_model, name)]
        except KeyError:
            obj = object.__new__(cls)
            Feature._cache[(binary_features_model, name)] = obj
            return obj
        if not isinstance(existing, cls):
            raise InvalidFeatureError(
                'Feature with this name exists but is of a different type')
        return existing
        
    def delete (self):
        """Deletes this feature, removing it from the
        `.BinaryFeaturesModel`."""
        self.binary_features_model._remove_feature(self)
        del Feature._cache[(self.binary_features_model, self.name)]
        self.binary_features_model = None

    def get_value_characters (self, value):
        """Returns the set of `.Character`\s that have `value` for this
        feature.

        :param value: feature value
        :type value: `str`
        :rtype: `set` of `.Character`\s

        """
        return self.binary_features_model.get_feature_value_characters(
            self, value)
    
    @property
    def name (self):
        """Returns the name of this feature.

        :rtype: `str`

        """
        return self._name

    @name.setter
    def name (self, name):
        """Sets the name of this feature.

        Raises `.InvalidFeatureError` if a `.Feature` with `name`
        already exists.
        
        :param name: name to be set
        :type name: `str`

        """
        if name == self.name:
            return
        if (self.binary_features_model, name) in Feature._cache:
            raise InvalidFeatureError('A feature with that name already exists')
        Feature._cache[(self.binary_features_model, name)] = self
        del Feature._cache[(self.binary_features_model, self.name)]
        self._name = name
