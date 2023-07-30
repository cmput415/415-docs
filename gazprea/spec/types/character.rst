.. _ssec:character:

Character
---------

A ``characters`` is a signed 8-bit value. A ``character`` can be
represented by an ``i8`` in *MLIR*.

.. _sssec:character_decl:

Declaration
~~~~~~~~~~~

A ``character`` value is declared with the keyword ``character``.

.. _sssec:character_null:

Null
~~~~

``null`` is ASCII ``NUL`` (``'\0'``, ``0x00``) for ``character``.

.. _sssec:character_ident:

Identity
~~~~~~~~

``identity`` is ASCII ``SOH`` (``0x01``) for characters. This choice allows
the casting of a ``character`` to an ``integer`` to yield the
``integer`` ``identity``.

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

There are no operations defined between scalar values with type``character``.
To operate on a ``character`` it must first be cast to either a ``boolean``,
``integer``, or ``real``.

However, scalar values with type ``character`` may still be concatenated onto
values with type ``string`` or vectors with type ``character``


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``character`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
