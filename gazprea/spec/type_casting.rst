.. _sec:typeCasting:

Type Casting
============

*Gazprea* provides explicit :term:`type casting`. Type casting is an
:term:`expression`. A value may be converted to a different type using the
following syntax where ``value`` is an expression and ``toType`` is the
destination type:

::

     as<toType>(value)

Conversion from one type to another is not always legal. For instance
converting from an ``integer`` array to an ``integer`` has no
reasonable conversion. Attempting such a conversion is a compile-time
error; the compiler must emit a ``TypeError`` (see :ref:`sec:errors`). More
generally, any ``as<>`` conversion this chapter does not describe as legal is
a compile-time error, and the compiler must emit a ``TypeError`` (see
:ref:`sec:errors`).

.. _ssec:typeCasting_stos:

Scalar to Scalar
----------------

This table summarizes all of the conversion rules between scalar types
where N/A means no conversion is possible, id means no change is
necessary, and anything else describes how to convert the value to the
new type. Attempting a conversion marked N/A is a compile-time error;
the compiler must emit a ``TypeError`` (see :ref:`sec:errors`):

+----------+-------------------------------------------------------------------------------------------------------------------------------------+
|          |                                                          **To type**                                                                |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          |           | boolean                        | character                      | integer                  | real                       |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | boolean   | id                             | '\\0' if false, 0x01 otherwise | 1 if true, 0 otherwise   | 1.0 if true, 0.0 otherwise |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **From** | character | false if '\\0', true otherwise | id                             | *ASCII* value as integer | *ASCII* value as real      |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
| **type** | integer   | false if 0, true otherwise     | unsigned integer value mod 256 | id                       |  real version of integer   |
|          +-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+
|          | real      | N/A                            | N/A                            | truncate                 |  id                        |
+----------+-----------+--------------------------------+--------------------------------+--------------------------+----------------------------+

.. _ssec:typeCasting_stovm:

Scalar to Array
-----------------------

A scalar may be explicitly cast to an array of any dimension with an element
type that the original scalar can be explicitly cast to according to the rules
in :ref:`ssec:typeCasting_stos`. A scalar to array cast *must* include a size
with the type to cast to as this cannot be inferred from the scalar value. For
example:

::

     // Create an array of reals with length three where all values are 1.0.
     real[*] v = as<real[3]>(1);

     // Create an array of booleans with length 10 where all values are true.
     var u = as<boolean[10]>('c');

.. _ssec:typeCasting_vtov:

Array to Array
----------------

Conversions between array types are also possible. First, the values of the
original are cast to the destination type's element type according to the rules
in :ref:`ssec:typeCasting_stos` and then the destination is padded with
destination element type's :term:`zero value` or truncated to match the
destination type size. Note that a concrete size is not required for array to
array casting: writing the destination element type with an unspecified length
(``[*]``) keeps the old size, so no padding or truncation occurs. Padding or
truncation happens only when a concrete size is given. For example:

::

     real[3] v = [i in 1..3 | i + 0.3 * i];

     // Convert the real array to an integer array.
     integer[3] u = as<integer[*]>(v);

     // Convert to integers and zero pad.
     integer[5] x = as<integer[5]>(v);

     // Truncate the array.
     real[2] y = as<real[2]>(v);

A cast of a non-variable empty array literal ``[]`` is :term:`ill-formed`,
because a literal empty array does not have a type.

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

.. _ssec:typeCasting_vec:

Array and Vector
----------------

A :ref:`vector <ssec:vector>` participates in ``as<>`` casts on both sides.

- As the **operand** of an array cast, a vector supplies its *current* length
  as the source size; the cast then pads with the element type's :term:`zero
  value` or truncates to the destination array's stated size, exactly as in
  :ref:`ssec:typeCasting_vtov`.

- As the **destination** type, a ``vector<T>`` takes no size specifier: the
  result simply has the length of the value being cast, so there is nothing
  to pad or truncate. Only the element type is converted, per
  :ref:`ssec:typeCasting_stos`.

- A :term:`scalar <scalar type>` may be cast directly to a ``vector<T>``
  destination, producing a single-element vector. Because a vector carries no
  size specifier, the element type ``T`` must be written explicitly -- there
  is no size or element-type inference for this cast.

::

     vector<real> v = [1.5, 2.5, 3.5];

     // Vector as operand: its current length (3) is the source size.
     integer[2] a = as<integer[2]>(v);             // [1, 2]  (truncated)
     integer[5] b = as<integer[5]>(v);             // [1, 2, 3, 0, 0]  (padded)

     // Vector as destination: no size; takes the value's length.
     integer[3] w = [4, 5, 6];
     vector<integer> u = as<vector<integer> >(w);  // [4, 5, 6]

     // Scalar to vector: single-element vector; T must be explicit.
     vector<integer> s = as<vector<integer> >(5);  // [5]

.. _ssec:typeCasting_ttot:

Tuple to Tuple
--------------

Conversions between ``tuple`` types are also possible. The source type and
the destination type must have an equal number of members, and each member
must be pairwise castable; a mismatch in the number of members, or a member
that cannot be cast under its own kind's rule, is a compile-time error and
the compiler must emit a ``TypeError`` (see :ref:`sec:errors`). Every
member is cast by the rule for its own kind: scalar members follow
:ref:`ssec:typeCasting_stos`, array members
follow :ref:`ssec:typeCasting_vtov` (including padding and truncation), and
a nested ``tuple``, ``vector``, or array member follows the same
cast rules as a standalone value of that type. A ``struct`` member is the
exception: a ``struct`` cannot be cast (see :ref:`ssec:struct`), so the two
struct types must be identical and the member is copied unchanged. For example:

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, boolean) rb_tup = as<tuple(real, boolean)>(int_tup);
