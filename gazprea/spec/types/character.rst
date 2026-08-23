.. _ssec:character:

Character
---------

A ``character`` is a signed 8-bit value. A ``character`` can be
represented by an ``i8`` in *MLIR*.

.. _sssec:character_decl:

Declaration
~~~~~~~~~~~

A ``character`` value is declared with the keyword ``character``.

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
Hex escape      ``\xH[H]``          ``0x00`` to ``0xFF``
=============== =================== ===============

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

:term:`Scalar <scalar type>` values with type ``character`` may be
concatenated onto values of type ``string`` or arrays with type
``character``. See :ref:`sssec:string_ops` for the full concatenation
rules, including the ``TypeError`` (see :ref:`sec:errors`) raised when
both operands of ``||`` are scalar, e.g. ``character || character``.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``character`` may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.
