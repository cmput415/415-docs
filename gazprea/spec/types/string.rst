.. _ssec:string:

String
------

A ``string`` is fundamentally an array of ``character``. However, there exists
several differences between the two types: an :ref:`extra declaration style
<sssec:string_decl>`, an :ref:`extra literal style <sssec:string_lit>`, the
:ref:`result of a concatenation <sssec:string_ops>` and :ref:`behaviour when
sent to an output stream <sssec:output_format>`.

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the keyword ``string``. The same rules of
:ref:`array declarations <sssec:array_decl>` also apply to strings, allowing
for both explicit and inferred size declarations:

::

  string[*] <identifier> = <type-string>;
  string[int-expr] <identifier> = <type-string>;

However, ``string`` variables have an extra method of writing an inferred size
declaration:

::

  string <identifier> = <type-string>;

.. _sssec:string_lit:

Literals
~~~~~~~~

Strings can be constructed in the same way as arrays using character literals.
*Gazprea* also provides a special syntax for string literals. A string literal
is any sequence of character literals (including escape sequences) in between
double quotes. For instance:

::

  string cats_meow = "The cat said \"Meow!\"\nThat was a good day.\n"

Although strings and character arrays look similar, they are still treated
differently by the compiler:

::

   character[*] vec = "hello world\n";
   vec -> std_output;

prints:

::

  [h e l l o   w o r l d
  ]

.. _sssec:string_ops:

Operations
~~~~~~~~~~

Strings have all of the same operations defined on them as the other array data
types, but with one extra addition. Because a ``string`` and array of
``character`` are fundamentally the same, the concatenation operation may be
used to concatenate values of the two types. As well, a scalar ``character`` may
be concatenated onto a ``string`` in the same way as it would be concatenated
onto an array of ``character``.

This operation should always result in a value with type ``string``. Again,
because a ``string`` is always able to be converted to an array of
``character``, this is only apparent when printing the result. For example:

::

  ['a', 'b'] || "cd" -> std_output;
  "ef" || 'g' -> std_output;

prints the following:

::

  abcdefg


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``string`` may be cast and/or promoted to, see the
sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` respectively.
