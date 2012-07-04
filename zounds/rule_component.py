class RuleComponent:

    """A representation of a component of a rule."""

    def __init__ (self):
        self._elements = []
    
    def append (self, element):
        """Appends `element` to this rule component."""
        self._elements.append(element)

    @property
    def applier_form (self):
        """Returns this rule component in a form suitable for use by
        an `.Applier`.

        :rtype: `str`

        """
        forms = []
        for element in self._elements:
            forms.append(element.applier_form)
        return ''.join(forms)
