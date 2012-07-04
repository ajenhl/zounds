from .rule_component import RuleComponent


class ContextRuleComponent (RuleComponent):

    @property
    def applier_form (self):
        """Returns this rule component in a form suitable for use by
        an `.Applier`.

        :rtype: `str`

        """
        forms = []
        for element in self._elements:
            forms.append(element.applier_form)
        if forms[0] == '^':
            insert_index = 1
        else:
            insert_index = 0
        forms.insert(insert_index, '(?P<start>')
        forms.append(')')
        return ''.join(forms)


