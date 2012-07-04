from .exceptions import IllegalArgumentError


class Date:

    _cache = set()

    def __init__ (self, ruleset, number, name):
        """Initialises this object.

        :param ruleset: the ruleset this date is associated with
        :type ruleset: `.Ruleset`
        :param number: numeric date (used for temporal ordering)
        :type number: `int`
        :param name: name of date (used for display)
        :type name: `str`

        """
        self._ruleset = ruleset
        self._number = number
        self._name = name

    def __new__ (cls, ruleset, number, name):
        Date._check_number_unique(ruleset, number)
        # If the name is not unique, the cache must have the
        # ruleset/number combination removed.
        try:
            Date._check_name_unique(ruleset, name)
        except IllegalArgumentError:
            Date._cache.remove((ruleset, number))
            raise
        return object.__new__(cls)

    def __lt__ (self, other):
        return self._number < other._number

    @staticmethod
    def _check_name_unique (ruleset, name, old_name=None):
        """Adds the combination of `ruleset` and `name` to the date cache.

        Raises `.IllegalArgumentError` if the combination exists in the
        cache.

        :param ruleset: ruleset
        :type ruleset: `.Ruleset`
        :param name: date name
        :type name: `str`
        :param old_name: optional date name to be removed from the cache
        :type old_name: `str`

        """
        if (ruleset, name) in Date._cache:
            raise IllegalArgumentError('Date with this name already exists')
        Date._cache.add((ruleset, name))
        if old_name is not None:
            Date._cache.remove((ruleset, old_name))

    @staticmethod
    def _check_number_unique (ruleset, number, old_number=None):
        """Adds the combination of `ruleset` and `number` to the date cache.

        Raises `.IllegalArgumentError` if the combination exists in the
        cache.

        :param ruleset: ruleset
        :type ruleset: `.Ruleset`
        :param number: numeric date
        :type number: `int`
        :param old_number: optional numeric date to be removed from
          the cache
        :type old_number: `int`

        """
        if (ruleset, number) in Date._cache:
            raise IllegalArgumentError('Date with this number already exists')
        Date._cache.add((ruleset, number))
        if old_number is not None:
            Date._cache.remove((ruleset, old_number))
    
    @property
    def name (self):
        """Returns the name of this date.

        :rtype: `str`

        """
        return self._name

    @name.setter
    def name (self, name):
        """Sets the name of this date.

        :param name: name of date
        :type name: `str`

        """
        Date._check_name_unique(self._ruleset, name, self._name)
        self._name = name
    
    @property
    def number (self):
        """Returns the numeric component of this date.

        :rtype: `int`

        """
        return self._number

    @number.setter
    def number (self, number):
        """Sets the numeric component of this date.

        :param number: numeric date
        :type number: `int`

        """
        Date._check_number_unique(self._ruleset, number, self._number)
        self._number = number
    
    def delete (self):
        """Deletes this date, removing it from its `.Ruleset` and any
        `.Language`\s it is associated with."""
        self._ruleset.remove_date(self)
        self._ruleset = None
