.. _sec:typeCasting:

Type Casting
============

*Gazprea* provides explicit type casting. Type casting is an expression. 
A value may be converted to a
different type using the following syntax where ``value`` is an
expression and ``toType`` is our destination type:

::

     as<toType>(value)

Conversion from one type to another is not always legal. For instance
converting from an ``integer`` array to an ``integer`` has no
reasonable conversion.

.. _ssec:typeCasting_stos:

Scalar to Scalar
----------------

This table summarizes all of the conversion rules between scalar types
where N/A means no conversion is possible, id means no change is
necessary, and anything else describes how to convert the value to the
new type:

+----------+-------------------------------------------------------------------------------------------------------------------------------------+
|          |                                                          **To type**                                                                |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          |           | boolean                        | character                      | integer                  | real                       |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | boolean   | id                             | ‘\\0’ if false, 0x01 otherwise | 1 if true, 0 otherwise   | 1.0 if true, 0.0 otherwise |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **From** | character | false if ‘\\0’, true otherwise | id                             | *ASCII* value as integer | *ASCII* value as real      |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **type** | integer   | false if 0, true otherwise     | unsigned integer value mod 256 | id                       |  real version of integer   |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | real      | N/A                            | N/A                            | truncate                 |  id                        |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+

.. _ssec:typeCasting_stovm:

Scalar to Array
-----------------------

A scalar may be promoted to an array of any dimension with an element type that
the original scalar can be cast to according to the rules in :ref:`ssec:typeCasting_stos`.
A scalar to array cast *must* include a size with the type to cast to as this
cannot be inferred from the scalar value. For example:

::

     // Create an array of reals with length three where all values are 1.0.
     real[*] v = as<real[3]>(1);

     // Create an array of booleans with length 10 where all values are true.
     var u = as<boolean[10]>('c');

.. _ssec:typeCasting_vtov:

Array to Array
----------------

Conversions between array types are also possible. First, the
values of the original are cast to the destination type’s element type
according to the rules in :ref:`ssec:typeCasting_stos` and then the destination
is padded with destination element type’s zero or truncated to match the
destination type size. Note that the size is not required for array to
array casting; if the size is not included in the cast type, the new
size is assumed to be the old size. For example:

::

     real[3] v = [i in 1..3 | i + 0.3 * i];

     // Convert the real array to an integer array.
     integer[3] u = as<integer[*]>(v);

     // Convert to integers and zero pad.
     integer[5] x = as<integer[5]>(v);

     // Truncate the array.
     real[2] y = as<real[2]>(v);

Note that a cast is the one place where a *shortening* is silent. Assigning a
too-long array value into an array raises a ``SizeError``; casting it to a
shorter array type truncates instead. The size named in the cast belongs to
the cast expression's result, and says nothing about the variable it is
eventually stored into — that variable's own length was already fixed at
:ref:`elaboration <sssec:array_sizing>`, and the cast result still has to fit
it.

::

     real[3] v = [1.0, 2.0, 3.0];
     var real[3] w = 0.0;

     w = as<real[2]>(v);  /* cast truncates to [1.0, 2.0], then pads back to
                             [1.0, 2.0, 0.0] to fit 'w' */

Casting non-variable empty arrays ``[]`` is not allowed, because a literal
empty array does not have a type.

.. _ssec:typeCasting_vec:

Array and Vector
----------------

A ``vector`` may appear as the operand of an array cast and as the destination
type of a cast. When a vector is the operand, its current length is used. When
``vector<T>`` is the destination type, no size may be given — vectors are
runtime sized and take the length of the value being cast, so there is nothing
to pad or truncate against.

::

     var vector<integer> v;
     v.append([1, 2, 3]);

     real[2] a = as<real[2]>(v);          // truncates to [1.0, 2.0]
     var vector<real> u = as<vector<real>>(v);  // [1.0, 2.0, 3.0]

.. _ssec:typeCasting_mtom:

Multi-dimensional Arrays
------------------------

Conversions between arrays of any dimension are possible.
The process is exactly like :ref:`ssec:typeCasting_vtov` except padding and
truncation can occur in all dimensions. For example:

::

     real[2][2] a = [[1.2, 24], [-13e2, 4.0]];

     // Convert to an integer matrix.
     integer[2][2] b = as<integer[2][2]>(a);

     // Convert to integers and pad in both dimensions.
     integer[3][3] c = as<integer[3][3]>(a);

     // Truncate in one dimension and pad in the other.
     real[1][3] d = as<real[1][3]>(a);
     real[3][1] e = as<real[3][1]>(a);

.. _ssec:typeCasting_ttot:

Tuple to Tuple
--------------

Conversions between ``tuple`` types are also possible. The original type
and the destination type must have an equal number of internal types and
each element must be pairwise castable according to the rules
in :ref:`ssec:typeCasting_stos`. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, boolean) rb_tup = as<tuple(real, boolean)>(int_tup);
