Binary Features Model
=====================

IPA Zounds uses a binary features model as the basis for a sound
change rule to express groups or classes of sounds. Other sound change
appliers use independent variables to achieve a similar result, but
only in a limited and ad hoc fashion.

IPA Zounds includes a binary features model, but users may write their
own to match their needs, as it is difficult if not impossible to
adequately cover all of the
:abbr:`IPA (International Phonetic Alphabet)`
in a single model with only binary features. Handling five vowel
heights, for example, is somewhat cumbersome (using three features,
``high``, ``mid`` and ``low``, with some combinations of feature
values being meaningless); to cope with seven would be worse.

Wikipedia's brief article provides more information on `distinctive
features`_.


File Format
-----------

The syntax for binary features model files, described in
:abbr:`EBNF (Extended Backus-Naur Form)` notation, is as follows
(whitespace between tokens not specified):

.. productionlist:: binary_features_model
   model: `base_features_section`, `base_characters_section`,
        : [ `diacritic_characters_section` ], [ `spacing_characters_section` ],
        : [ `suprasegmental_features_section`, `suprasegmental_characters_section` ] ;
   base_features_section: "[Base Features]", `features` ;
   base_characters_section: "[Base Characters]", `base_character_features`,
                          : { `base_character_features` } ;
   base_character_features: `base_character`, ":", [ `feature_list` ] ;
   diacritic_characters_section: "[Diacritic Characters]", `diacritic_character_values`,
                               : { `diacritic_character_values` }
   diacritic_character_values: `diacritic_character`, ":", `valued_feature_list` ;
   spacing_characters_section: "[Spacing Characters]", `spacing_character_values`,
                             : { `spacing_character_values` } ;
   spacing_character_values: `spacing_character`, ":", `valued_feature_list` ;
   suprasegmental_features_section: "[Suprasegmental Features]", `features` ;
   suprasegmental_characters_section: "[Suprasegmental Characters]", `suprasegmental_character_values`,
                                    : { `suprasegmental_character_values` } ;
   suprasegmental_character_values: `suprasegmental_character`, ":", `valued_feature_list` ;
   feature_list: { `feature`, "," }, `feature` ;
   valued_feature_list: { `valued_feature`, "," }, `valued_feature` ;
   valued_feature: `feature_value`, `feature` ;
   feature_value: "+" | "-" | "−" ;
   features: `feature`, { `feature` } ;
   feature: ? alphabetic_character ?, { ? alphabetic_character ? } ;
   base_character: ? Unicode IPA base character ? ;
   diacritic_character: ? Unicode IPA diacritic character ? ;
   spacing_character: ? Unicode IPA spacing character ? ;
   suprasegmental_character: ? Unicode IPA suprasegmental character ? ;
   alphabetic_character: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" |
                       : "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" |
                       : "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" |
                       : "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" |
                       : "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" |
                       : "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;

A :token:`feature` must not be duplicated within either the
:token:`base_features_section` or
:token:`suprasegmental_features_section`, nor across those two
productions.

The :token:`feature_list` is a list of those features that a character
possesses.

The actual characters that are recognised are listed in the API
documentation: :obj:`~zounds.constants.BASE_CHARACTERS`,
:obj:`~zounds.constants.DIACRITIC_CHARACTERS`,
:obj:`~zounds.constants.SPACING_CHARACTERS`, and
:obj:`~zounds.constants.SUPRASEGMENTAL_CHARACTERS`. These constants
may be changed if desired.

An example::

  [Base Features]
  anterior
  consonantal
  voiced

  [Base Characters]
  a: anterior, voiced
  p: anterior, consonantal

  [Diacritic Characters]
  ̥ : -voiced

  [Suprasegmental Features]
  long

  [Suprasegmental Characters]
  ː: +long


.. _distinctive features: https://secure.wikimedia.org/wikipedia/en/wiki/Distinctive_feature
