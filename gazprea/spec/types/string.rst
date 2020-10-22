.. _ssec:string:

String
------

A string is simply an array of characters. The only difference between a
character vector and a string is the behaviour when sent to an :ref:`output stream <sssec:output_format>`.

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the type ``string``, and is followed by an optional size specifier.
The same rules of :ref:`vector declarations <sssec:vector_decl>` also apply to strings, just
substitute ``string`` for the ``<type>``.

But note one minor addition: there are two methods of declaring a string of inferred size, both depicted below.

::

		string <identifier> = <type-string>;
		string[*] <identifier> = <type-string>;

.. _sssec:string_null:

Null
~~~~

Same behaviour as ``null`` for vectors. The string is filled with ``null``
characters.

.. _sssec:string_ident:

Identity
~~~~~~~~

Same behaviour as ``identity`` for vectors. The string is filled with
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
vector data types, but with one caveat:

The concatenation operation ``||`` between a ``string`` and a ``vector`` of ``character``\ s and vice-versa results in a ``string``.
For example:

::

	['a', 'b'] || "cd" -> std_output;

prints the following:

::

	abcd


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``string`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
