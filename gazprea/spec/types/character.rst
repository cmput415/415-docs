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
character enclosed in single quotes. You may not use literal newlines.
For example:

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
=============== =================== ===============

.. _sssec:character_ops:

Operations
~~~~~~~~~~

The following operations are defined between ``character`` values. 

+------------+--------------------------+------------+---------------------------+-------------------+
| **Class**  | **Operation**            | **Symbol** | **Usage**                 | **Associativity** |
+============+==========================+============+===========================+===================+
| Grouping   | parentheses              | ``()``     | ``(character)``           | N/A               |
+------------+--------------------------+------------+---------------------------+-------------------+
| Comparison | equals                   | ``==``     | ``character == character``| left              |
|            +--------------------------+------------+---------------------------+-------------------+
|            | not equals               | ``!=``     | ``character != character``| left              |
+------------+--------------------------+------------+---------------------------+-------------------+

Scalar values with type ``character`` may be concatenated onto
values with type ``string`` or arrays with type ``character``.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``character`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
