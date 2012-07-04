from .exceptions import IllegalArgumentError


class Language:

    _cache = set()

    def __init__ (self, ruleset, name):
        self._ruleset = ruleset
        self._name = name
        self._ruleset.add_language(self)

    def __lt__ (self, other):
        # For sorting purposes.
        return self.name < other.name

    def __new__ (cls, ruleset, name):
        Language._check_name_unique(ruleset, name)
        return object.__new__(cls)
    
    def add_date (self, date):
        """Adds `date` to this language.

        :param date: date to add
        :type date: `.Date`

        """
        self._ruleset.add_date_to_language(self, date)

    def add_rule (self, date, rule):
        """Adds `rule` to this language at `date`.

        :param date: date at which rule occurs
        :type date: `.Date`
        :param rule: rule to add
        :type rule: `.Rule`

        """
        self._ruleset.add_rule(self, date, rule)

    @staticmethod
    def _check_name_unique (ruleset, name, old_name=None):
        """Adds the combination of `ruleset` and `name` to the language cache.

        Raises `.IllegalArgumentError` if the combination exists in the
        cache.

        :param ruleset: ruleset
        :type ruleset: `.Ruleset`
        :param name: language name
        :type name: `str`
        :param old_name: optional language name to be removed from cache
        :type old_name: `str`

        """
        if (ruleset, name) in Language._cache:
            raise IllegalArgumentError('Language with this name already exists')
        Language._cache.add((ruleset, name))
        if old_name is not None:
            Language._cache.remove((ruleset, old_name))

    @property
    def dates (self):
        """Returns the dates associated with this language.

        Dates are returned in temporal order, earliest to latest.
        
        :rtype: `list` of `.Date`\s

        """
        return self._ruleset.get_language_dates(self)
        
    def delete (self):
        """Deletes this language, removing it from its `.Ruleset`."""
        self._ruleset.remove_language(self)
        self._ruleset = None
    
    @property
    def name (self):
        """Returns the name of this language.

        :rtype: `str`

        """
        return self._name

    @name.setter
    def name (self, name):
        """Sets the name of this language.

        :param name: name to set
        :type name: `str`

        """
        Language._check_name_unique(self._ruleset, name, self._name)
        self._name = name

    def remove_date (self, date):
        """Removes `date` from this language.

        :param date: date to remove
        :type date: `.Date`

        """
        self._ruleset.remove_date_from_language(self, date)
