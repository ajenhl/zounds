from .rule_element import RuleElement


class Placeholder (RuleElement):

    def __init__ (self, binary_features_model, source_component):
        """Initialises this placeholder.
        
        :param binary_features_model: binary features model
        :type binary_features_model: `.BinaryFeaturesModel`
        :param source_component: source component this is a placeholder for
        :type source_component: `.SourceRuleComponent`

        """
        super().__init__(binary_features_model)
        self._source_component = source_component

    @property
    def applier_form (self):
        """Returns this element in a form suitable for use by an
        `.Applier`.

        :rtype: `str`

        """
        return ')(?P<match>{})(?='.format(self._source_component.applier_form)
