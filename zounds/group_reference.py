from .rule_element import RuleElement
from .source_rule_component import SourceRuleComponent


class GroupReference (RuleElement):

    def __init__ (self, index, rule_component_class):
        """Initialises a GroupReference object.

        :param index: index of the group this object references
        :type index: `int`
        :param rule_component: type of rule component that this
          grouping reference is in
        :type rule_component: `type`

        """
        self._elements = []
        self._group_name = 'group{}'.format(index)
        if rule_component_class == SourceRuleComponent:
            self._context = r'(?P=%s%s)'
        else:
            self._context = r'\g<%s%s>'

    def append (self, element):
        self._elements.append(element)

    @property
    def applier_form (self):
        element_content = ''.join([element.applier_form for element in
                                   self._elements])
        return self._context.format(self._group_name, element_content)
