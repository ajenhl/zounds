# Characters specifying whether a character has a feature, does not
# have it, or has no relationship with it. Used in the normalised form
# of a character/cluster and as keys in the binary features model
# dictionaries.
#: Symbol specifying that a character possesses a feature.
HAS_FEATURE = '1'
#: Symbol specifying that a character has no relationship with a
#: feature. This value is not allowed for a base character.
INAPPLICABLE_FEATURE = '2'
#: Symbol specifying that a character does not possess a feature.
NOT_HAS_FEATURE = '0'

#: Applier form marker, indicating the start of a new normalised form
#: sequence.
AFM = 'M'
#: Marker for the beginning of a normalised form sequence for a
#: base (non-suprasegmental) character/cluster.
BNFM = 'B'
#: Marker for the beginning of a normalised form sequence for a
#: suprasegmental character/cluster.
SNFM = 'S'

#: Forwards direction through time (ascending date numbers).
FORWARDS = 'forwards'
#: Backwards direction through time (descending date numbers).
BACKWARDS = 'backwards'

#: Symbols usable as homorganic variables.
HOMORGANIC_VARIABLES = [
    'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο',
    'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']

#: Symbol used to specify where in a context rule component the source
#: component occurs.
SOURCE_PLACEHOLDER = '_'

#: Symbol used to divide rule components within a rule.
RULE_COMPONENT_DIVIDER = '/'

#: Symbol marking the start of a base feature set.
OPEN_BASE_FEATURE_SET = '['
#: Symbol marking the end of a base feature set.
CLOSE_BASE_FEATURE_SET = ']'

#: Symbol marking the start of a suprasegmental feature set.
OPEN_SUPRASEGMENTAL_FEATURE_SET = '<'
#: Symbol marking the end of a suprasegmental feature set.
CLOSE_SUPRASEGMENTAL_FEATURE_SET = '>'

#: Symbol marking the start of an optional set of rule elements.
OPEN_OPTIONAL = '('
#: Symbol marking the end of an optional set of rule elements.
CLOSE_OPTIONAL = ')'

#: Symbol marking the start of a group of rule elements.
OPEN_GROUP = '{'
#: Symbol marking the end of a group of rule elements.
CLOSE_GROUP = '}'

#: Valid symbols to be used as base characters.
BASE_CHARACTERS = [
    'p', 'b', 't', 'd', 'ʈ', 'ɖ', 'c', 'ɟ', 'k', 'g', 'q', 'ɢ', 'ʔ', 'm', 'ɱ',
    'n', 'ɳ', 'ɲ', 'ŋ', 'ɴ', 'ʙ', 'r', 'ʀ', 'ɾ', 'ɽ', 'ɸ', 'β', 'f', 'v', 'θ',
    'ð', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ', 'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ',
    'h', 'ɦ', 'ɬ', 'ɮ', 'ʋ', 'ɹ', 'ɻ', 'j', 'ɰ', 'l', 'ɭ', 'ʎ', 'ʟ', 'i', 'y',
    'ɨ', 'ʉ', 'ɯ', 'u', 'ɪ', 'ʏ', 'ʊ', 'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o', 'ə', 'ɛ',
    'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ', 'æ', 'ɐ', 'a', 'ɶ', 'ɑ', 'ɒ', 'ʘ', 'ǀ', 'ǃ', 'ǂ',
    'ǁ', 'ɓ', 'ɗ', 'ʄ', 'ɠ', 'ʛ', 'ʍ', 'w', 'ɥ', 'ʜ', 'ʢ', 'ʡ', 'ɕ', 'ʑ', 'ɺ',
    'ɧ', 'ʣ', 'ʤ', 'ʦ', 'ʧ']

#: Valid symbols to be used as diacritic characters.
#:
#: These strings include an initial space, to prevent the character
#: from composing with the initial quote mark.
#:
#: U+0306, the extra-short length marker, is included here as well as
#: with the suprasegmental characters. In this automated context,
#: length may be more conveniently handled as a base feature, and not a
#: suprasegmental one.
DIACRITIC_CHARACTERS = [
    ' ̥', ' ̬', ' ̹', ' ̜', ' ̟', ' ̠', ' ̈', ' ̽', ' ̩', ' ̯', ' ̤', ' ̰',
    ' ̼', ' ̝', ' ̞', ' ̘', ' ̙', ' ̪', ' ̺', ' ̻', ' ̃', ' ̚', ' ̋', ' ̄',
    ' ̱', ' ̏', ' ́', ' ̀', ' ̂', ' ̌', ' ̆']

#: Valid symbols to be used as spacing characters.
#:
#: Includes tone markers that may be used in place of the non-contoured
#: diacritic tone characters.
#:
#: Includes length markers that are also allowed as suprasegmental
#: characters. In this automated context, length may be more
#: conveniently handled as a base feature, and not a suprasegmental
#: one.
SPACING_CHARACTERS = ['ʰ', '˞', 'ʷ', 'ʲ', 'ˠ', 'ˤ', '̴', 'ⁿ', 'ˡ', '˥', '˦',
                      '˧', '˨', '˩', '↓', '↑', '↗', '↘', 'ː', 'ˑ']

#: Valid symbols to be used as suprasegmental characters.
SUPRASEGMENTAL_CHARACTERS = ['ˈ', 'ˌ', 'ː', 'ˑ', '̆', '|', '‖', '.']
