.. _sec:typeCasting:

Type Casting
============

*Gazprea* provides explicit type casting. A value may be converted to a
different type using the following syntax where ``value`` is an
expression and ``toType`` is our destination type:

::

     as<toType>(value)

Conversions from one type to another is not always legal. For instance
converting from an ``integer`` ``matrix`` to an ``integer`` has no
reasonable conversion.

.. _ssec:typeCasting_stos:

Scalar to Scalar
----------------

This table summarizes all of the conversion rules between scalar types
where N/A means no conversion is possible, id means no change is
necessary, and anything else describes how to convert the value to the
new type:

+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|                      |                                              **To type**                                                                |
+                      +--------------------------------+--------------------------------+--------------------------+----------------------------+
|                      | boolean                        | character                      | integer                  | real                       |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | boolean   | id                             | ‘\\0’ if false, 0x01 otherwise | 1 if true, 0 otherwise   | 1.0 if true, 0.0 otherwise |
+          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **From** | character | false if ‘\\0’, true otherwise | id                             | *ASCII* value as integer | *ASCII* value as real      |
+          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **type** | integer   | false if 0, true otherwise     | unsigned integer value mod 256 | id                       |  real version of integer   |
+          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | real      | N/A                            | N/A                            | truncate                 |  id                        |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+

.. _ssec:typecasting_stovm:

Scalar to Vector/Matrix
-----------------------

[ssec:typecasting_stov] [ssec:typecasting_stom] A scalar may be promoted
to either a ``vector`` or ``matrix`` with an element type that the
original scalar can be cast to according to the rules in . A scalar to
vector cast *must* include a size with the type to cast to as this
cannot be inferred from the scalar value. For example:

::

     // Create a vector of reals with length three where all values are 1.0.
     real vector v = as<real vector[3]>(1);

     // Create a vector of booleans with length 10 where all values are true.
     var u = as<boolean vector[10]>('c');

.. _ssec:typeCasting_itov:

Interval to Vector
------------------

An ``integer`` ``interval`` may be explicitly cast to an ``integer`` or
``real`` ``vector`` as in the , but the explicit cast can cause the
interval to be truncated or ``null`` padded.

.. _ssec:typeCasting_vtov:

Vector to Vector
----------------

Conversions between ``vector`` types are also possible. First, the
values of the original are casted to the destination type’s element type
according to the rules in and then the destination is padded with
destination element type’s ``null`` or truncated to match the
destination type size. Note that the size is not required for vector to
vector casting; if the size is not included in the cast type, the new
size is assumed to be the old size. For example:

::

     real vector v[3] = [i in 1..3 | i + 0.3 * i];

     // Convert the real vector to an integer vector.
     integer vector u[3] = as<integer vector>(v);

     // Convert to integers and null pad.
     integer vector x[5] = as<integer[5]>(v);

     // Truncate the vector.
     real vector y[2] = as<real vector[2]>(v);

.. _ssec:typeCasting_mtom:

Matrix to Matrix
----------------

Conversions between ``matrix`` types are also possible. The process is
exactly like except padding and truncation can occur in both dimensions.
For example:

::

     real matrix a[2, 2] = [[1.2, 24], [-13e2, 4.0]];

     // Convert to an integer matrix.
     integer matrix b[2, 2] = as<integer matrix[2, 2]>(a);

     // Convert to integers and pad in both dimensions.
     integer matrix c[3, 3] = as<integer matrix[3, 3]>(a);

     // Truncate in one dimension and pad in the other.
     real matrix d[1, 3] = as<real matrix[1, 3]>(a);
     real matrix e[3, 1] = as<real matrix[3, 1]>(a);

.. _ssec:typeCasting_ttot:

Tuple to Tuple
--------------

Conversions between ``tuple`` types are also possible. The original type
and the destination type must have an equal number of internal types and
each element must be pairwise castable according to the rules in . For
example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, boolean) rb_tup = as<tuple(real, boolean)>(int_tup);
