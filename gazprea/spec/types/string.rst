.. _ssec:string:

String
------

A ``string`` is another object within *Gazprea*. Fundamentally, a ``string`` is
a ``vector`` of ``character``.
This means a string is **runtime sized** in exactly the way a
:ref:`vector <ssec:vector>` is — its length is never part of its type and
changes as it is assigned to, pushed to, or appended to — but because it is an
object *Gazprea* can provide type specific features.
A ``character[N]`` array is the fixed-length counterpart: its length is settled
at elaboration and stays there.

String vectors behave a lot like character arrays, but there are several
differences between the two types:
an :ref:`extra literal style <sssec:string_lit>`,
the :ref:`result of a concatenation <sssec:string_ops>`
and :ref:`behaviour when sent to an output stream <sssec:output_format>`.

.. _sssec:string_decl:

Declaration
~~~~~~~~~~~

A string may be declared with the keyword ``string``. The same rules of
:ref:`vector declarations <sssec:vec_decl>` also apply to strings, which means
that no length may be written in the type and the length is always whatever the
string currently holds:

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

   character[*] carray = ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '\n'];
   string vec = carray;
   carray -> std_output;
   vec -> std_output;

prints:

::

  [h e l l o   w o r l d
  ]
  hello world


.. _sssec:string_ops:

Operations
~~~~~~~~~~

As character vectors, strings have all of the same operations defined on them as
the other array data types.
Remember that because a ``string`` and vector of ``character`` are fundamentally
the same, the concatenation operation may be used to concatenate values of the
two types. You may also append a slice of characters to a string using the
append method.
As well, a scalar character may be concatenated onto a string in the same way
as it would be concatenated onto an array of characters.
Note the difference between the two spellings. ``||`` is an operator: it
produces a new value and leaves its operands alone, which is why it is the only
option for arrays. Because a ``string`` is a sub-type of ``vector``, a string
can instead be *grown in place* with the ``append`` and ``push`` methods:

::

  var string letters = ['a', 'b'] || "cd";
  letters.append("ef");
  letters.push('g');
  letters  -> std_output;

prints the following:

::

  abcdefg


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``string`` may be cast and/or promoted to, see the
sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` respectively.
