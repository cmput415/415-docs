.. _ssec:string:

String
------

A ``String`` is another object within *Gazprea*. Fundamentally, a ``String``
is a ``Vector`` of ``character``. This means that, like a vector, a string
behaves like a dynamically sized array, but because it is an object *Gazprea*
can provide type specific features.

However, there exists
several differences between the two types: an :ref:`extra declaration style
<sssec:string_decl>`, an :ref:`extra literal style <sssec:string_lit>`, the
:ref:`result of a concatenation <sssec:string_ops>` and :ref:`behaviour when
sent to an output stream <sssec:output_format>`.

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the keyword ``String``. The same rules of
:ref:`vector declarations <sssec:vec_decl>` also apply to strings, which means
that all lenghts are inferred:

::

  String <identifier> = <type-string>;

.. _sssec:string_lit:

Literals
~~~~~~~~

Strings can be constructed in the same way as arrays using character literals.
*Gazprea* also provides a special syntax for string literals. A string literal
is any sequence of character literals (including escape sequences) in between
double quotes. For instance:

::

  String cats_meow = "The cat said \"Meow!\"\nThat was a good day.\n"

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

As character arrays, strings have all of the same operations defined on them as
the other array data types, Remember that because a ``String`` and array of
``character`` are fundamentally the same, the concatenation operation may be
used to concatenate values of the two types.
As well, a scalar ``character`` may be concatenated onto a ``String`` in the
same way as it would be concatenated onto an array of ``character``.
Note that because a ``String`` is a type of ``Vector``, concatenation may
also be accomplished with ``concat`` and ``push`` methods:

::

  String letters = ['a', 'b'] || "cd";
  letters.concat("ef");
  letters.push('g');
  letters  -> std_output;

prints the following:

::

  abcdefg


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``String`` may be cast and/or promoted to, see the
sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` respectively.
