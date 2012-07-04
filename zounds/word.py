class Word:

    """A representation of a word in a particular language at a
    particular time.

    A Word may have relationships to other Words, backwards and
    forwards in time, representing the next possible or actual Word in
    a chain of sound changes. Multiple such relationships are possible
    in either direction: in a chain from the forward applier, to
    multiple immediate descendants in different languages; in a chain
    from the reverse applied, to multiple possible immediate parents.

    A Word can be rendered for display as IPA, or in any specified
    script.
    
    """

    def __init__ (self, clusters, language, date):
        """Initialise this word.

        :param clusters: the clusters that make up this word
        :type clusters: `list` of `.Cluster`\s
        :param language: language of this word
        :type language: `.Language`
        :param date: date of this word
        :type date: `.Date`

        """
        self._clusters = clusters
        self._language = language
        self._date = date
        self._ipa = ''.join([str(cluster) for cluster in clusters])

    @property
    def date (self):
        """Returns the date of this word.

        :rtype: `.Date`

        """
        return self._date

    @date.setter
    def date (self, date):
        """Sets the date of this word.

        :param date: date to set
        :type date: `.Date`

        """
        self._date = date

    def get_display_form (self, script=None):
        """Returns a display form of this word.

        If `script` is None, IPA is used; otherwise it is rendered in
        `script`.

        :param script: optional script to use for rendering
        :type script: `.Script`
        :rtype: `str`

        """
        if script is None:
            return self._ipa

    def get_scripts (self):
        """Returns a list of `.Script`\s that are 'native' for this word.

        'Native' scripts are those associated with the language and
        date combination of this word.

        :rtype: `list` of `.Script`\s

        """
        pass
    
    @property
    def language (self):
        """Returns the language of this word.

        :rtype: `.Language`

        """
        return self._language

    @language.setter
    def language (self, language):
        """Sets the language of this word.

        :param language: language to set
        :type language: `.Language`

        """
        self._language = language
