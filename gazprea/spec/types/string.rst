.. _ssec:string:

String
------

A string is just a type synonym for a vector of characters.

.. _sssec:string_declr:

Declaration
~~~~~~~~~~~

A string may be declared with the type ``string``. ``string`` is a built-n
typedef for character vector.

.. _sssec:string_null:

Null
~~~~

Same behaviour as ``null`` for vectors. Vector filled with ``null``
characters.

.. _sssec:string_ident:

Identity
~~~~~~~~

Same behaviour as ``identity`` for vectors. Vector filled with
``identity`` characters.

.. _sssec:string_lit:

Literals
~~~~~~~~

Strings can be constructed in the same way as vectors using character
literals. *Gazprea* also provides a special syntax for string literals.
A string literal is any sequence of character literals (including escape
sequences) in between double quotes. For instance:

::

   				string cats_meow = "The cat said \"Meow!\"\nThat was a good day.\n"
   			

.. _sssec:string_ops:

Operations
~~~~~~~~~~

Strings have all of the same operations defined on them as the other
vector data types.


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``string`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` 
respectively.