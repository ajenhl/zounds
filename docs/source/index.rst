.. IPA Zounds documentation master file, created by
   sphinx-quickstart on Sun Sep 18 15:37:23 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to IPA Zounds's documentation!
======================================

IPA Zounds is a sound change applier: a program that models linguistic
sound change by applying sound change rules to a list of words. It
uses a binary features model of the
:abbr:`IPA (International Phonetic Alphabet)`,
allowing users to write words and rules using
:abbr:`IPA (International Phonetic Alphabet)`
characters and the distinctive features of the model.

So, for example, a rule to lengthen any vowel before a final voiced
postalveolar fricative would be written as::

   [+syllabic]/[+long]/_ʒ#

Contents
--------

.. toctree::
   :maxdepth: 1

   binary_features_model
   rule
   api/zounds

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

