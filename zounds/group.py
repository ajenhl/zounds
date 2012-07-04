from .container_rule_element import ContainerRuleElement
from .exceptions import IllegalArgumentError


class Group (ContainerRuleElement):

    def __init__ (self, binary_features_model, index):
        """Initialise this `.Group`.

        :param binary_features_model: binary features model
        :type binary_features_model: `.BinaryFeaturesModel`
        :param index: index of the group this object references
        :type index: `int`

        """
        super().__init__(binary_features_model)
        self._group_name = 'group{}'.format(index)

    def append (self, element):
        """Appends `element` to this element's contents.

        :param element: element to add
        :type element: `.RuleElement`

        """
        if isinstance(element, Group):
            # QAZ: error message.
            raise IllegalArgumentError
        super().append(element)
        
    @property
    def applier_form (self):
        """Returns this element in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        element_content = ''.join([element.applier_form for element in
                                   self._elements])
        return '(?P<{}>{})'.format(self._group_name, element_content)
