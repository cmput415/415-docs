.. _sec:implicitCasts:

Implicit Casts
==============

An *implicit cast* is a conversion the compiler performs automatically,
with no syntax in the program text. Implicit casts are the counterpart of
the *explicit casts* written ``as<toType>(value)`` in
:ref:`sec:typeCasting`; "cast" is the umbrella term for both.

Most conversions that can be performed implicitly can also be written
explicitly as an ``as<>`` cast. The one caveat is that a scalar-to-array
*explicit cast* must state the destination size explicitly
(:ref:`ssec:typeCasting_stovm`), whereas the corresponding *implicit cast*
takes its size from the array operand. (The ``string`` / ``character[*]``
conversion, being the array/vector cast specialized to ``character``, has
both an implicit and an explicit ``as<>`` form like any other array/vector
cast; see :ref:`ssec:implicitCasts_string`.)

A :term:`scalar <scalar type>` may be implicitly cast to an array of any
rank, including the rank-2 matrix case (see :ref:`ssec:implicitCasts_stoa`).
An array is never implicitly cast to a different rank; only a scalar expands
to fill an array or matrix.

Attempting any conversion this chapter does not describe as a valid implicit
cast -- in a declaration, an assignment, or between corresponding tuple
members -- is a compile-time error; the compiler must emit a ``TypeError``
(see :ref:`sec:errors`).

.. _ssec:implicitCasts_scalar:

Scalars
-------

The only automatic implicit cast between scalars is ``integer`` to
``real``. This cast is one way -- a ``real`` is never implicitly cast to
``integer``.

Automatic conversion follows this table where N/A means no implicit cast is
possible, id means no conversion necessary, and ``as<toType>(value)`` means the
value of type "From type" is converted to type "toType" using semantics from
:ref:`sec:typeCasting`.

+----------+-----------+---------+-----------+---------+---------------+
|          |                    **To type**                            |
+----------+-----------+---------+-----------+---------+---------------+
|          |           | boolean | character | integer |     real      |
+          +-----------+---------+-----------+---------+---------------+
| **From** |  boolean  |   id    |    N/A    |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
| **type** | character |   N/A   |    id     |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
|          |  integer  |   N/A   |    N/A    |   id    |as<real>(value)|
+          +-----------+---------+-----------+---------+---------------+
|          |   real    |   N/A   |    N/A    |   N/A   |      id       |
+----------+-----------+---------+-----------+---------+---------------+

Because ``character`` and ``integer`` are N/A in both directions, there is no
implicit cast between them. A direct consequence is that ``character`` values
are **not orderable**: the relational operators ``<``, ``>``, ``<=``, ``>=``
are undefined on characters, and ordering them requires an explicit
``as<integer>(...)`` cast (see :ref:`ssec:character` and :ref:`sec:typeCasting`).

.. _ssec:implicitCasts_stoa:

Scalar to Array
--------------------------

All scalar types can be implicitly cast to arrays whose element type the
scalar can be :ref:`implicitly cast to <ssec:implicitCasts_scalar>`.
This can occur when an array is used in an operation with a scalar value.

The scalar is implicitly cast to an array matching the array operand's size
(the operand-size rule of :ref:`sssec:array_ops`); the result's element
type is whichever type the operation requires, and the scalar is first
implicitly cast to that element type. For example:

::

     integer i = 1;
     integer[*] v = [1, 2, 3, 4, 5];
     integer[*] res = v + i;

     res -> std_output;

would print the following:

::

     [2 3 4 5 6]

Other examples:

::

  1 == [1, 1]  // true
  1..2 || 3 // [1, 2, 3]

Concatenation (``||``) is an exception to the size-matching rule above: a
scalar operand becomes a single new element regardless of the other
operand's length, rather than being expanded to match it (see
:ref:`sssec:string_ops`).

Note that an array can never be cast down to a scalar, even explicitly.
Also note that matrix multiply imposes strict requirements on the
dimensionality of the operands. The consequence is that, *as an operand of
matrix multiplication* (``**``), a scalar can only be implicitly cast to a
matrix when the other operand is a square matrix (:math:`m \times m`): the
scalar is then broadcast (filled) into an :math:`m \times m` matrix whose every
element equals the scalar. For higher-rank arrays this generalizes only to
hypercubes with all extents equal; *Gazprea* provides no comprehensive
broadcasting, so a scalar cannot be broadcast to a non-square matrix operand of
``**`` at all. In element-wise operations and initializations a scalar is
implicitly cast to an array (or matrix) of any dimensions.

.. _ssec:implicitCasts_ttot:

Tuple to Tuple
--------------

A tuple may be implicitly cast to another tuple type when the two have an equal
number of members and each member of the source can be implicitly cast to the
corresponding member of the destination. Each member is cast by the rule for
its own kind: scalar members follow the scalar table above, array members
follow the :ref:`array sizing rules <sssec:array_sizing>` -- a shorter value is
padded with the element type's :term:`zero value` and a longer value raises a
``SizeError`` (see :ref:`sec:errors`). A nested ``tuple``, ``vector``, or
array member follows the same implicit-cast rules as a standalone value of that
type. A ``struct`` member is the exception: a ``struct`` is never implicitly
cast (see :ref:`ssec:struct`), so the two struct types must be identical and
the member is copied unchanged. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;

     tuple(character, integer, boolean[2]) many_tup = ('a', 1, [true, false]);
     tuple(character, real, boolean[2]) other_tup = many_tup;

If initializing a variable with a tuple via :ref:`sec:typeInference`, the
variable is inferred to have the same type as the tuple initializer.
Therefore, tuple elements are also copied accordingly. For example:

::

     tuple(real, real) foo = (1, 2);
     tuple(real, real) bar = (3, 4);

     var baz = foo;
     baz.1 -> std_output; // 1.0
     baz.2 -> std_output; // 2.0

     baz = bar;
     baz.1 -> std_output; // 3.0
     baz.2 -> std_output; // 4.0


It is possible for a two-sided implicit cast to occur with tuples. For
example:

::

  boolean b = (1.0, 2) == (2, 3.0);

.. _ssec:implicitCasts_avv:

Array to/from Vector
--------------------

An array value and a :ref:`vector <ssec:vector>` are implicitly cast to one
another in both directions. Like every implicit cast this converts a
*value*; it never changes how either side is sized. Each element converts by
the implicit-cast rule for its own type: the scalar table of
:ref:`ssec:implicitCasts_scalar` for a scalar element, or the corresponding
rule elsewhere in this chapter, applied recursively, for a composite element
type.

- **Vector to array.** The vector's *current* length produces the array
  value. Storing that value into an array obeys the array's own
  :ref:`fixed length <sssec:array_sizing>`: a shorter value is padded with
  the element type's :term:`zero value` and a longer value raises a
  ``SizeError`` (see :ref:`sec:errors`). If the destination is an inferred
  ``[*]`` array and this is its :term:`initialization`, the vector's current
  length becomes that array's fixed length.

- **Array to vector.** The array's fixed length produces the vector value.
  The receiving vector takes that length and may still grow afterwards via
  ``push``/``append``.

::

     vector<integer> vec = [1, 2, 3];       // current length 3
     integer[3] a = vec;                    // [1, 2, 3]
     integer[5] b = vec;                    // [1, 2, 3, 0, 0]  (padded)
     integer[*] c = vec;                    // length inferred as 3, then fixed

     integer[2] d = [7, 8];
     var vector<integer> w = d;             // [7, 8]; w may still grow
     call w.push(9);                        // [7, 8, 9]

.. _ssec:implicitCasts_atoa:

Array to Array
--------------

An array value may be implicitly cast to another array type of the **same
rank** when every element can be implicitly cast to the destination's element
type. Each element converts by the implicit-cast rule for its own type (the
scalar table of :ref:`ssec:implicitCasts_scalar` for scalar elements, applied
recursively for composite elements). The result obeys the destination array's
:ref:`fixed length <sssec:array_sizing>`: a shorter value is padded with the
element type's :term:`zero value` and a longer value raises a ``SizeError``
(see :ref:`sec:errors`). An array is never implicitly cast to a different
rank.

::

     integer[3] v = [1, 2, 3];
     real[3] u = v;                         // [1.0, 2.0, 3.0]

.. _ssec:implicitCasts_string:

Character Array to/from String
-------------------------------

A ``string`` value can be implicitly cast to a ``character`` array
(``character[*]``) and vice versa (a two-way implicit cast). Because a
``string`` is a language-supplied typealias for ``vector<character>`` (see
:ref:`ssec:string`), this is simply the array/vector implicit cast of
:ref:`ssec:implicitCasts_avv` specialized to the ``character`` element type;
the conversion of note is between ``string`` and character *arrays*.

::

     string str1 = "Hello"; /* str1 == "Hello" */
     character[*] chars = str1; /* chars == ['H', 'e', 'l', 'l', 'o'] */
     string str2 = chars || [' ', 'W', 'o', 'r', 'l', 'd']; /* str2 == "Hello World" */
