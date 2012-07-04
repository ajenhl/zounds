from collections import MutableSequence

from .exceptions import MismatchedModelsError
from .rule_element import RuleElement


class ContainerRuleElement (RuleElement, MutableSequence):

    """A representation of a rule element that may contain other rule
    elements.

    Uses the Abstract Base Class `collections.MutableSequence` to
    provide an implementation of the sequence of contained elements.

    """

    def __init__ (self, binary_features_model):
        super().__init__(binary_features_model)
        self._elements = []
    
    def __delitem__ (self, key):
        del self._elements[key]

    def __getitem__ (self, key):
        return self._elements[key]

    def __len__ (self):
        return len(self._elements)

    def __setitem__ (self, key, value):
        self._elements[key] = value

    def append (self, element):
        if element.binary_features_model != self._binary_features_model:
            raise MismatchedModelsError
        super().append(element)

    def insert (self, index, value):
        self._elements.insert(index, value)
