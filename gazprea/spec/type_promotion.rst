.. _sec:typePromotion:

Type Promotion
==============

:term:`Type promotion` is *Gazprea*'s implicit type-conversion mechanism.
It is deliberately distinct from :ref:`type casting <sec:typeCasting>`,
which is the explicit mechanism invoked via ``as<toType>(value)``.

Most conversions that can be done implicitly via promotion can also be done
explicitly via a typecast expression. There are two caveats. First, a
scalar-to-array *cast* must state the destination size explicitly
(:ref:`ssec:typeCasting_stovm`), whereas the corresponding *promotion*
infers the size from the array operand. Second, the
``string``/``character[*]`` conversion is an implicit two-way promotion
with no ``as<>`` form (see the final section of this chapter).

Note that there is no implicit promotion from a one-dimensional array to a
two-dimensional array: only scalars broadcast, to arrays and to matrices
alike.

.. _ssec:typePromotion_scalar:

Scalars
-------

The only automatic type promotion for scalars is ``integer`` to
``real``. This promotion is one way - a ``real`` cannot be automatically
converted to ``integer``.

Automatic type conversion follows this table where N/A means no implicit
conversion possible, id means no conversion necessary,
``as<toType>(var)`` means var of type "From type" is converted to type
"toType" using semantics from :ref:`sec:typeCasting`.

+----------+-----------+---------+-----------+---------+---------------+
|          |                    **To type**                            |
+----------+-----------+---------+-----------+---------+---------------+
|          |           | boolean | character | integer |     real      |
+          +-----------+---------+-----------+---------+---------------+
| **From** |  boolean  |   id    |    N/A    |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
| **type** | character |   N/A   |    id     |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
|          |  integer  |   N/A   |    N/A    |   id    | as<real>(var) |
+          +-----------+---------+-----------+---------+---------------+
|          |   real    |   N/A   |    N/A    |   N/A   |      id       |
+----------+-----------+---------+-----------+---------+---------------+

.. _ssec:typePromotion_stoa:

Scalar to Array
--------------------------

All scalar types can be promoted to arrays that have an internal type that the
scalar can be :ref:`converted to implicity <ssec:typePromotion_scalar>`.
This can occur when an array is used in an operation with a scalar value.

The scalar will be implicitly converted to an array of
equivalent dimensions and equivalent internal type. For example:

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

  1 == [1, 1]  // True
  1..2 || 3 // [1, 2, 3]

Note that an array can never be downcast to a scalar,
even if type casting is used. Also note that matrix multiply imposes strict
requirements on the dimensionality of the operands. The consequence is
that, *as an operand of matrix multiplication* (``**``), a scalar can only
be promoted to a matrix when the other operand is a square matrix
(:math:`m \times m`). In element-wise operations and initializations a
scalar broadcasts to a matrix of any shape.

Tuple to Tuple
--------------

Tuples may be promoted to another tuple type if it has an equal number of
internal types and the original internal types can be implicitly
converted to the new internal types. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;

     tuple(character, integer, boolean[2]) many_tup = ('a', 1, [true, false]);
     tuple(character, real, boolean[2]) other_tup = many_tup;

If initializing a variable with a tuple via :ref:`sec:typeInference`, the
variable is assumed to be the same type.
Therefore, tuple elements also copied accordingly. For example:

::

     tuple(real, real) foo = (1, 2);
     tuple(real, real) bar = (3, 4);

     var baz = foo;
     baz.1 -> std_output; // 1
     baz.2 -> std_output; // 2

     baz = bar;
     baz.1 -> std_output; // 3
     baz.2 -> std_output; // 4


It is possible for a two sided promotion to occur with tuples. For example:

::

  boolean b = (1.0, 2) == (2, 3.0);

Character Array to/from String
-------------------------------

A ``string`` can be implicitly converted to a ``character`` array
(``character[*]``) and vice-versa (two-way type promotion). Because a
``string`` is itself a vector of ``character`` (see :ref:`ssec:string`),
the conversion of note is between ``string`` and character *arrays*; a
``string`` used where a character array is expected, or vice-versa,
converts silently.

::

     string str1 = "Hello"; /* str1 == "Hello" */
     character[*] chars = str1; /* chars == ['H', 'e', 'l', 'l', 'o'] */
     string str2 = chars || [' ', 'W', 'o', 'r', 'l', 'd']; /* str2 == "Hello World" */
