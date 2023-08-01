.. _sec:typePromotion:

Type Promotion
==============

Type promotion is a sub-problem of casting and refers to casts that happen
implicitly.

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

All scalar types can be promoted to ``vector`` or ``matrix`` types that
have an internal type that the scalar can be :ref:`converted to implicity <ssec:typePromotion_scalar>`. This can occur when a
``vector`` or ``matrix`` is used in an operation with a scalar value.

The scalar will be implicitly converted to a ``vector`` or ``matrix`` of
equivalent dimensions and equivalent internal type. For example:

::

     integer i = 1;
     integer[*] v = [1, 2, 3, 4, 5];
     integer[*] res = v + i;

     res -> std_output;

would print the following:

::

     [2 3 4 5 6]

.. _ssec:typePromotion_ivltov:

Interval to Vector
------------------

An ``interval`` can be implicitly converted to an identically-sized
``vector`` of any type that ``integer`` can be :ref:`converted to implicity <ssec:typePromotion_scalar>`. For example:

::

     integer interval i = 1..5;
     integer[5] iv = i;
     real[*] rv = i;

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

A ``string`` can be implicitly converted to a ``vector`` of ``character``\ s and vice-versa (two-way type promotion).

::

     string str1 = "Hello"; /* str == "Hello" */
     character[*] chars = str; /* chars == ['H', 'e', 'l', 'l', 'o'] */
     string str2 = chars || [' ', 'W', 'o', 'r', 'l', 'd']; /* str2 == "Hello World" */
