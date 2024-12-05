.. _sec:typePromotion:

Type Promotion
==============

Type promotion is a sub-problem of casting and refers to casts that happen
implicitly.

Any conversion that can be done implicitly via promotion can also be done explicitly via typecast expression.
The notable exception is vector to matrix promotion, which occurs as a consequence of scalar to vector promotion
since a matrix is effectively a vector of vectors.

.. _ssec:typePromotion_scalar:

Scalars
-------

The only automatic type promotion for scalars is ``integer`` to
``real``. This promotion is one way - a ``real`` cannot be automatically
converted to ``integer``.

Automatic type conversion follows this table where N/A means no implicit
conversion possible, id means no conversion necessary,
``as<toType>(var)`` means var of type "From type" is converted to type
"toType" using semantics from .

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

.. _ssec:typePromotion_stov:

Scalar to Vector or Matrix
--------------------------

All scalar types can be promoted to vector or matrix types that
have an internal type that the scalar can be :ref:`converted to implicity <ssec:typePromotion_scalar>`. This can occur when a
vector or matrix is used in an operation with a scalar value.

The scalar will be implicitly converted to a vector or matrix of
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

Note that a vector or matrix can never be downcast to a scalar, even if
type casting is used. Also note that matrix multiply imposes strict
requirements on the dimensionality of the the operands. The consequence is
that scalars can only be promoted to a matrix if the matrix multiply
operand is a square matrix (:math:`m \times m`).

.. _ssec:typePromotion_stov:

Vector to Matrix
--------------------------

Vector to matrix promotion occurs because a row in a matrix is equivalent to
a vector. When a matrix is initialized or operated with a vector, each scalar
element in the vector is interpreted as a row. By applying the scalar to
vector promotion rule, each scalar element in the vector will be promoted
to a vector,becoming a row. The example below demonstrates scalar to row promotion,
row padding and column padding all together.

::
  
    integer[3,4] m1 = [1,[1,2,3]];
    // m1 = [[1, 1, 1, 1], [1, 2, 3, 0], [0, 0, 0, 0]]
    

The number of columns in each row are inferred, first by the expression
indicating the column size in the type declaration, and second, if the columnn
size is inferred as ``*``, by the size of the vector literal or expression.
Therefore, when the column size is infered, a vector to matrix promotion always
produces a square matrix.

::

    integer[2, *] m2 = [3, 4];
    // m2 = [[3, 3], [4, 4]]

Vector to matrix promotions apply in all contexts where operations on matricies are defined.

.. _ssec:typePromotion_ttot:

Tuple to Tuple
--------------

Tuples may be promoted to another tuple type if it has an equal number of
internal types and the original internal types can be implicitly
converted to the new internal types. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;

     tuple(char, integer, boolean[2]) many_tup = ('a', 1, [true, false]);
     tuple(char, real, boolean[2]) other_tup = many_tup;

Field names of tuples are overwritten by the field names of the left-hand side in assignments and declarations when promoted. For example:

::

     tuple(integer a, real b) foo = (1, 2);
     tuple(real c, real) bar = foo;

     foo.a -> std_output; // 1
     foo.b -> std_output; // 2

     bar.a -> std_output; // error
     bar.b -> std_output; // error
     bar.c -> std_output; // 1


If initializing a variable with a tuple via :ref:`sec:typeInference`, the variable is assumed to be the same type. Therefore, field names are also copied over accordingly. For example:

::

     tuple(real a, real b) foo = (1, 2);
     tuple(real c, real d) bar = (3, 4);

     var baz = foo;
     baz.a -> std_output; // 1
     baz.b -> std_output; // 2

     baz = bar;
     baz.a -> std_output; // 3
     baz.b -> std_output; // 4


It is possible for a two sided promotion to occur with tuples. For example:

::

  boolean b = (1.0, 2) == (2, 3.0);

Character Vector to/from String
-------------------------------

A ``string`` can be implicitly converted to a vector of ``character``\ s and vice-versa (two-way type promotion).

::

     string str1 = "Hello"; /* str == "Hello" */
     character[*] chars = str; /* chars == ['H', 'e', 'l', 'l', 'o'] */
     string str2 = chars || [' ', 'W', 'o', 'r', 'l', 'd']; /* str2 == "Hello World" */
