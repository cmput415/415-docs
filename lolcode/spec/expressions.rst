Expressions
-----------

Math
~~~~

The basic math operators are binary prefix operators:

::

    SUM OF <x> AN <y>       BTW +
    DIFF OF <x> AN <y>      BTW -
    PRODUKT OF <x> AN <y>   BTW *
    QUOSHUNT OF <x> AN <y>  BTW /
    MOD OF <x> AN <y>       BTW modulo


where ``<x>`` and ``<y>`` may each be expressions in the above, so mathematical operators can be nested and grouped indefinitely.

Math is performed as integer math in the presence of two ``NUMBR`` s.
If either of the arguments is a ``YARN``, the ``YARN`` is
converted to an integer and the operation proceeds if the conversion succeeds.

Conditions
~~~~~~~~~~

LOLCODE supports two conditional operators:

::

    BIGGR OF <x> AN <y>     BTW max
    SMALLR OF <x> AN <y>    BTW min

These operators apply to both strings and integers. Since both types are
supported, the types of ``<x>`` and ``<y>`` must match.

Concatenation
~~~~~~~~~~~~~

An indefinite number of YARNs may be explicitly concatenated with the ``SMOOSH...MKAY`` operator.
Arguments may optionally be separated with ``AN``.
As the ``SMOOSH`` expects strings as its input arguments, it will implicitly cast all input values of other types to ``YARN`` s.
The line ending may safely implicitly close the ``SMOOSH`` operator without needing an ``MKAY``.

