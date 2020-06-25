.. _sec:typePromotion:

Type Promotion
==============

Type promotion is a sub-problem to and refers to casts that happen
implicitly without extra syntax such as using ``as``.

**Assertion:** Implicit type conversions not found in will not be
performed. (`limited-promotion <#limited-promotion>`__)

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
have an internal type that the scalar can be . This can occur when a
``vector`` or ``matrix`` is used in an operation with a scalar value.

The scalar will be implicitly converted to a ``vector`` or ``matrix`` of
equivalent dimensions and equivalent internal type. For example:

::

     integer i = 1;
     integer vector v = [1, 2, 3, 4, 5];
     integer vector res = v + i;

     var out = std_output();
     res -> out;

would print the following:

::

     [2 3 4 5 6]

.. _ssec:typePromotion_ivltov:

Interval to Vector
------------------

An ``interval`` can be implicitly converted to an identically-sized
``vector`` of any type that ``integer`` can be . For example:

::

     integer interval i = 1..5;
     integer vector iv[5] = i;
     real vector rv = i;

.. _ssec:typePromotion_ttot:

Tuple to Tuple
--------------

Tuples may be promoted to another type if it has an equal number of
internal types and the original internal types can be implicitly
converted to the new internal types. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;

     tuple(char, integer, boolean[2]) many_tup = ('a', 1, [true, false]);
     tuple(char, real, boolean[2]) other_tup = many_tup;
