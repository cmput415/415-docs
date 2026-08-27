.. _ssec:character:

Character
---------

A ``character`` is an 8-bit value. A ``character`` can be
represented by an ``i8`` in *MLIR*. When a ``character`` is cast to
``integer`` or ``real`` its bit pattern is interpreted as an *unsigned* byte,
so its numeric value ranges from ``0`` to ``255`` (for example ``'\xFF'`` casts
to ``255``, not ``-1``); see :ref:`sec:typeCasting`.

.. _sssec:character_decl:

Declaration
~~~~~~~~~~~

A ``character`` value is declared with the keyword ``character``. If the
variable is not initialized explicitly, it is set to the null character
``'\0'`` (its :term:`zero value`).

.. _sssec:character_lit:

Literals and Escape Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``character`` literal is written in the same manner as *C99*: a single
character enclosed in single quotes. For example:

::

     'a'
     'b'
     'A'
     '1'
     '.'
     '*'

As in *C99*, *Gazprea* supports character escape sequences for common
characters. For example:

::

     '\0'
     '\n'

The following escape sequences are supported by *Gazprea*:

=============== =================== ===============
**Description** **Escape Sequence** **Value (Hex)**
=============== =================== ===============
Null            ``\0``               ``0x00``
Bell            ``\a``               ``0x07``
Backspace       ``\b``               ``0x08``
Tab             ``\t``               ``0x09``
Line Feed       ``\n``               ``0x0A``
Carriage Return ``\r``               ``0x0D``
Quotation Mark  ``\"``               ``0x22``
Apostrophe      ``\'``               ``0x27``
Backslash       ``\\``               ``0x5C``
Hex escape      ``\xH...``          ``0x00`` to ``0xFF``
=============== =================== ===============

A hex escape consumes all consecutive hexadecimal digits that follow ``\x`` and
must have at least one. A ``\x`` with no following hex digit, or an escape whose
value exceeds ``0xFF`` (255, the largest ``character``), is :term:`ill-formed`,
and the compiler must emit a ``LiteralError`` (see :ref:`sec:errors`).

.. _sssec:character_ops:

Operations
~~~~~~~~~~

The following operations are defined between ``character`` values.

+------------+---------------+------------+----------------------------+
| **Class**  | **Operation** | **Symbol** | **Usage**                  |
+============+===============+============+============================+
| Grouping   | parentheses   | ``()``     | ``(character)``            |
+------------+---------------+------------+----------------------------+
| Comparison | equals        | ``==``     | ``character == character`` |
|            +---------------+------------+----------------------------+
|            | not equals    | ``!=``     | ``character != character`` |
+------------+---------------+------------+----------------------------+

``character`` values are **not orderable**: the relational operators ``<``,
``>``, ``<=``, and ``>=`` are not defined on characters (only ``==`` and
``!=`` are), and there is no implicit cast between ``character`` and
``integer`` (see :ref:`sec:implicitCasts`). Applying a relational operator to
characters is therefore a ``TypeError`` (see :ref:`sec:errors`). To order
characters -- for example to test ``'a' <= c and c <= 'z'`` -- explicitly cast
each operand to ``integer`` with ``as<integer>(...)`` (see
:ref:`sec:typeCasting`), which yields the character's unsigned byte value.

:term:`Scalar <scalar type>` values with type ``character`` may be
concatenated onto values of type ``string`` or arrays with type
``character``; a ``character`` scalar is itself promoted to a single-element
``character`` array when concatenated, so ``character || character`` yields a
two-element ``character`` array (not a ``string``). See :ref:`sssec:string_ops`
for the full concatenation rules.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``character`` may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.
