class Ruleset:

    def __init__ (self, binary_features_model):
        self._binary_features_model = binary_features_model
        # Dictionary with language keys and dictionary values, with
        # date keys and list of rules values.
        self._data = {}

    def add_date_to_language (self, language, date):
        """Adds `date` to `language`.

        This method should only be called by a `.Language` object.

        :param language: language to add `date` to
        :type language: `.Language`
        :param date: date to add to `language`
        :type date: `.Date`

        """
        self._data[language][date] = []
        
    def add_language (self, language):
        """Adds `language` to the ruleset.

        This method should only be called by a `.Language` object.
        
        :param language: language to add
        :type language: `.Language`

        """
        self._data[language] = {}

    def add_rule (self, language, date, rule):
        """Adds `rule` to `language` at `date`.

        This method should only be called by a `.Language` object.

        :param language: language rule is to be added to
        :type language: `.Language`
        :param date: date rule is to be added at
        :type date: `.Date`
        :param rule: rule to add
        :type rule: `.Rule`

        """
        self._data[language][date].append(rule)

    def get_first_rules (self, language, date, direction):
        """Returns the first `.Rule`\s in `language` at `date`.

        If `direction` is `.BACKWARDS`, the sequence of rules is
        reversed, so that the "first" is the latest at `date`.

        If there is no matching `.Rule`, the next (in `direction`)
        `.Date` is tried. Language branching is followed, so multiple
        `.Rule`\s may be returned.

        :param language: the language the rule applies to
        :type: language: `.Language`
        :param date: the date the rule applies to
        :type date: `.Date`
        :param direction: the direction time is being travelled through
        :type direction: `str`
        :rtype: `list` of `.Rule`\s

        """
        pass

    def get_language_dates (self, language):
        """Returns the dates associated with `language`.

        Dates are returned in temporal order, earliest to latest.

        :param language: the language whose dates are to be returned
        :type language: `.Language`
        :rtype: `list` of `.Date`\s

        """
        return sorted(self._data[language].keys())

    def get_rules (self, language, date):
        """Returns the rules, in `.FORWARDS` direction, in `language`
        at `date`.

        :param language: the language the rule applies to
        :type: language: `.Language`
        :param date: the date the rule applies to
        :type date: `.Date`
        :rtype: `list` of `.Rule`\s

        """
        return self._data[language][date]

    @property
    def languages (self):
        """Returns the languages in this ruleset.

        The languages are returned in alphabetical order.
        
        :rtype: `list` of `.Language`\s

        """
        languages = list(self._data.keys())
        languages.sort()
        return languages
    
    def remove_date (self, date):
        """Removes `date` from the ruleset.

        :param date: date to remove
        :type date: `.Date`

        """
        for language in self.languages:
            language.remove_date(date)

    def remove_date_from_language (self, language, date):
        """Removes `date` from `language`.

        :param language: language to remove date from
        :type language: `.Language`
        :param date: date to remove from language
        :type date: `.Date`

        """
        self._data[language].pop(date, None)
    
    def remove_language (self, language):
        """Removes `language` from the ruleset.

        :param language: language to remove
        :type language: `.Language`

        """
        del self._data[language]
