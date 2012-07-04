from .exceptions import IllegalArgumentError
from .container_rule_element import ContainerRuleElement


class Optional (ContainerRuleElement):

    """A representation of an optional list of rule elements."""
    
    def __init__ (self, binary_features_model):
        super().__init__(binary_features_model)
        self._is_multiple = False

    def append (self, element):
        """Appends `element` to this element's contents.

        :param element: element to add
        :type element: `.RuleElement`

        """
        if isinstance(element, ContainerRuleElement):
            # QAZ: error message.
            raise IllegalArgumentError
        super().append(element)

    @property
    def applier_form (self):
        """Returns this element in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        if self.match_multiple:
            match_sign = '*'
        else:
            match_sign = '?'
        element_content = ''.join([element.applier_form for element
                                   in self._elements])
        return '({}){}'.format(element_content, match_sign)
        
    @property
    def match_multiple (self):
        """Returns True if the elements in this optional element may
        be matched multiple times.

        :rtype: `bool`

        """
        return self._is_multiple

    @match_multiple.setter
    def match_multiple (self, value):
        """Sets whether the elements in this optional element may be
        matched multiple times.

        :param value: value to set
        :type value: `bool`

        """
        self._is_multiple = value
