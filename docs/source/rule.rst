Sound change rules
==================

A sound change rule specifies how a particular sound changes (that is,
to what new sound it changes) within a specific context. A rule is
written in a rules file in the form::

   Rule a/b/c

where ``a`` is the sound to be changed (the source component), ``b``
is what ``a`` is to be changed to (the result component), and ``c`` is
the context in which ``a`` occurs (the context component). The source
component ``a`` may be empty, in which case ``b`` is added wherever
``c`` occurs. The result component ``b`` may be empty, in which case
``a`` is deleted. The context component ``c`` may be empty (save for
the placeholder, representing where the source component ``a``
occurs), in which case all instances of ``a`` are changed.

Note about overlapping matches (ana matches only once within banana).

Rule elements
-------------

Various elements may occur within each component, as detailed below.

Binary Feature Set
^^^^^^^^^^^^^^^^^^

A set of binary feature values applying to a single sound, thereby
representing the set of phonemes that share those feature values. For
example, ``[-long+nasal]`` denotes all those phonemes that are both
nasal and not long.

Note that a binary feature set does *not* mark a modification of the
previous phoneme, but rather represents a new, distinct phoneme or set
of phonemes. ``a[+nasal]`` does not represent a nasalised /a/, but
rather /a/ followed by any nasal phoneme.

May occur within all three components.

Represented by enclosing the feature values within square brackets,
e.g. ``[-anterior+voiced]``. ``[]`` represents any sound.

Placeholder
^^^^^^^^^^^

Specifies where within a context the source sound occurs.

May only occur within the context component.

Represented by ``_``.

