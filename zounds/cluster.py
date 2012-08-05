from .constants import AFM
from .exceptions import IllegalArgumentError
from .base_normalised_form import BaseNormalisedForm
from .rule_element import RuleElement
from .suprasegmental_normalised_form import SuprasegmentalNormalisedForm
from .word_element import WordElement


class Cluster (RuleElement, WordElement):

    """A Cluster is the combination of either a single base character
    with zero or more spacing and diacritic characters or one or more
    suprasegmental characters."""

    @staticmethod
    def __new__ (cls, binary_features_model, normalised_form=None):
        if isinstance(normalised_form, BaseNormalisedForm):
            from .base_cluster import BaseCluster
            subcls = BaseCluster
        elif isinstance(normalised_form, SuprasegmentalNormalisedForm):
            from .suprasegmental_cluster import SuprasegmentalCluster
            subcls = SuprasegmentalCluster
        else:
            # QAZ: error message
            raise IllegalArgumentError()
        return object.__new__(subcls)

    @property
    def applier_form (self):
        """Returns this cluster in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        return '{}{}'.format(AFM, self.normalised_form)

    @property
    def normalised_form (self):
        """Returns the normalised form of this cluster.

        :rtype: `.NormalisedForm`

        """
        raise NotImplementedError


class Counter:

    """Class for keeping track of the frequency of members in a
    list."""

    def __init__ (self):
        self._count = {}

    def add (self, item):
        """Adds an item to the list."""
        self._count[item] = self._count.get(item, 0) + 1

    def get_sorted (self):
        """Returns a reverse sorted list of items."""
        result = list(self._count.keys())
        result.sort(key=self._count.get, reverse=True)
        return result
