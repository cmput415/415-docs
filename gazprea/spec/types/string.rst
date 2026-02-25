.. _ssec:string:

String
------

A ``string`` is a distinct type in *Gazprea* that behaves as a wrapper around a
dynamically-sized ``character`` array. It is structurally equivalent to
``character[*]`` for all operations, but the type is preserved by the compiler
because it affects output formatting: a ``string`` written to an output stream
is printed as a sequence of characters (e.g. ``hello world``), while a
``character[*]`` is printed with array notation (e.g. ``[h e l l o]``).

Bi-directional promotion between ``string`` and ``character[*]`` is implicit,
meaning a ``string`` can be assigned to a ``character[*]`` variable and vice
versa without an explicit cast.

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the keyword ``string``. Because strings are
always dynamically sized, no length is specified in the declaration:

::

  string <identifier> = <string-expr>;

.. _sssec:string_lit:

Literals
~~~~~~~~

Strings can be constructed in the same way as character arrays by enclosing a
comma-separated list of character literals in square brackets. *Gazprea* also
provides a special string literal syntax: any sequence of characters (including
escape sequences) enclosed in double quotes.

::

  string cats_meow = "The cat said \"Meow!\"\nThat was a good day.\n";

Although strings and character arrays look similar, they are treated differently
at output:

::

   character[*] carray = ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '\n'];
   string s = carray;
   carray -> std_output;
   s -> std_output;

prints:

::

  [h e l l o   w o r l d
  ]
  hello world


.. _sssec:string_ops:

Operations
~~~~~~~~~~

Because a ``string`` is structurally equivalent to ``character[*]``, all array
operations apply to strings. Concatenation uses the ``||`` operator:

::

  var string greeting = "hello";
  var string full = greeting || " world";
  full -> std_output;  // Prints: hello world

A ``string`` and a ``character[*]`` may be concatenated directly using ``||``,
since bi-directional promotion makes them compatible, and the result of
concatenating two strings can itself be concatenated further:

::

  var string letters = ['h', 'e', 'l'] || "lo ";
  var string full = letters || "world";
  full -> std_output;  // Prints: hello world

A scalar ``character`` may also be concatenated onto a ``string`` through
scalar-to-array promotion:

::

  var string s = "abc";
  s = s || 'd';
  s -> std_output;  // Prints: abcd

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``string`` may be cast and/or promoted to, see the
sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` respectively.
