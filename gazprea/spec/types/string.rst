.. _ssec:string:

String
------

A ``string`` is a language-supplied *typealias* for ``vector<character>``:
the two are the same type by strong equivalence, not a distinct sub-type.
Anything true of a ``vector<character>`` is therefore true of a ``string``,
and the two may be used interchangeably *except for their print format*.

Because a ``string`` *is* a ``vector``, it is runtime-sized and unbounded
like any other vector: its length is simply the length of its underlying
character sequence, which may grow (for example through the ``push`` and
``append`` methods). There is no separate sized or bounded string type.
Growth needs a mutable receiver, though: ``push`` and ``append`` require a
``var`` string, and a ``string`` is ``const`` by
default, so a ``const string`` (or one whose qualifier is elided) is effectively
fixed for its lifetime:

::

   var string greeting = "hi";
   call greeting.append(" there");   // greeting == "hi there"
   call greeting.push('!');          // greeting == "hi there!"

   const string fixed = "constant";  // const by default; it cannot grow

Although a ``string`` and a plain ``character`` array/vector
behave alike in most
respects, *Gazprea* still treats the two differently in a couple of places:
strings have an :ref:`extra literal style <sssec:string_lit>` and special
:ref:`behavior when sent to an output stream <sssec:output_format>`.
(Concatenation is *not* one of these differences -- see
:ref:`sssec:string_ops`.)

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the keyword ``string``. The same rules of
:ref:`vector declarations <sssec:vec_decl>` also apply to strings, which means
that all lengths are inferred:

::

  [<qualifier>] string <identifier>;
  [<qualifier>] string <identifier> = <type-expr>;
  [<qualifier>] string <identifier> = <type-array>;

.. _sssec:string_lit:

Literals
~~~~~~~~

Strings can be constructed in the same way as arrays using character literals.
*Gazprea* also provides a special syntax for string literals. A string literal
is any sequence of character literals (including escape sequences) in between
double quotes. For instance:

::

  string cats_meow = "The cat said \"Meow!\"\nThat was a good day.\n";

Although strings and character arrays look similar, they are still treated
differently by the compiler:

::

   character[*] carray = ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '\n'];
   string vec = carray;
   vector<character> charvec = carray;
   carray -> std_output;
   charvec -> std_output;
   vec -> std_output;

prints:

::

  [h e l l o   w o r l d
  ][h e l l o   w o r l d
  ]
  hello world


.. _sssec:string_ops:

Operations
~~~~~~~~~~

As character vectors, strings have all of the same operations defined on them
as the other array data types. Remember that because a ``string`` *is* a
``vector<character>``, the concatenation operator ``||`` may be used to combine
``string`` values with ``character`` arrays (which are a distinct array type).
Concatenation takes the kind of its :ref:`receiver <sssec:array_ops>`, the
rightmost operand: when that receiver is a ``string`` (or any vector), the whole
concatenation is a ``string``, so ``"x = " || format(x)`` is a ``string`` and
prints as text when sent to a stream. When instead the receiver is a
``character`` array, the result is a ``character`` array, which is implicitly
cast back to a ``string`` whenever it is stored into one (see
:ref:`ssec:implicitCasts_string`). Either way
``var string letters = ['a', 'b'] || "cd";`` below is legal -- here its receiver
``"cd"`` is a ``string``, so the concatenation is itself a ``string``. Every
:term:`scalar <scalar type>` operand of ``||`` is promoted to a single-element
array of its type, so no operand need be composite and two scalars may be
concatenated: ``character || character`` yields a two-element ``character``
array -- never a ``string``, and never a ``TypeError``. Because the result is a
``string`` only when the rightmost operand already is one, a scalar character on
the right, as in ``"ab" || 'c'``, gives a ``character`` array, whereas
``"ab" || "c"`` gives a ``string``. You may also append a slice of
characters to a string using the append method. As well, a scalar character may
be concatenated onto a string in the same way as it would be concatenated onto
an array of characters. Note that because ``string`` is a typealias for
``vector<character>``, concatenation may also be accomplished with the
``append`` and ``push`` methods (see :ref:`sssec:vec_methods`; strings have
exactly the vector method set):

::

  var string letters = ['a', 'b'] || "cd";
  call letters.append("ef");
  call letters.push('g');
  letters  -> std_output;

prints the following:

::

  abcdefg

Operator precedence and associativity are specified once, for all types,
in the :ref:`table of operator precedence <ssec:expressions_toop>`.


Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that a ``string`` may be cast to -- explicitly with
``as<>()`` or through an implicit cast -- see the sections on
:ref:`sec:typeCasting` and :ref:`sec:implicitCasts` respectively.
