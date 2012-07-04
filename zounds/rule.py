import re


class Rule:

    """A representation of a sound change rule.

    A rule consists of three components: the source (the part of a
    word to change), the context (the surrounding context of the
    source), and the result (what the source changes into). The source
    and result components may each be empty (but not both within the
    same rule). The context component must contain a source
    placeholder.

    A rule is associated with a language and a date, and has a place
    in the sequence of rules within the language/date combination.

    Each rule is unique, even if two rules have the same components
    and the same language and date.

    A rule has links to the next rules in sequence, going both forward
    and back in time. There may be multiple next rules due to language
    branching.
    
    """

    def __init__ (self, language, date, source, context, result):
        """Initialise this rule.

        :param language: language this rule applies to
        :type language: `.Language`
        :param date: date this rule is applies to
        :type date: `.Date`
        :param source: source component
        :type source: `.SourceRuleComponent`
        :param context: context component
        :type context: `.ContextRuleComponent`
        :param result: result component
        :type result: `.ResultRuleComponent`

        """
        self._language = language
        self._date = date
        self._source = source
        self._context = context
        self._result = result
        self._language.add_rule(date, self)

    @property
    def applier_form (self):
        """Returns this rule in a form suitable for use by an
        `.Applier`.

        :rtype: `._sre.SRE_Pattern`

        """
        return re.compile(self._context.applier_form)

    @property
    def date (self):
        """Returns the date of this rule.

        :rtype: `.Date`

        """
        return self._date

    def get_display (self):
        """Returns this rule in presentational format.

        :rtype: `list` of `str`
        
        """
        pass
    
    def get_next_rules (self, direction):
        """Returns the next rules in sequence.

        `direction` specifies whether the next rules are forward or
        backwards in time.

        Due to language branching, multiple rules may be returned.

        :param direction: the direction time is being travelled through
        :type direction: `str`
        :rtype: `list` of `.Rule`\s

        """
        pass

    @property
    def language (self):
        """Returns the language of this rule.

        :rtype: `Language`

        """
        return self._language
