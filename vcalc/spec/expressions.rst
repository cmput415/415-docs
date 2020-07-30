Expressions
-----------

Operators
~~~~~~~~~

Because we’ve added a new binary operator, we need to update our
precedence table. Operators without a horizontal line dividing them have
equal precedence. For example, addition and subtraction have an equal
level of precedence.

+------------+----------------+------------+------------------+-------------------+
| **Class**  | **Operation**  | **Symbol** | **Usage**        | **Associativity** |
+============+================+============+==================+===================+
| Vector     | index          | []         | ``expr[expr]``   | left              |
+            +----------------+------------+------------------+-------------------+
|            | range          | \..        | ``expr .. expr`` | left              |
+------------+----------------+------------+------------------+-------------------+
| Arithmetic | multiplication | \*         | ``expr * expr``  | left              |
|            |                |            |                  |                   |
|            | division       | /          | ``expr / expr``  | left              |
+            +----------------+------------+------------------+-------------------+
|            | addition       | \+         | ``expr + expr``  | left              |
|            |                |            |                  |                   |
|            | subtraction    | \-         | ``expr - expr``  | left              |
+------------+----------------+------------+------------------+-------------------+
| Comparison | less than      | <          | ``expr < expr``  | left              |
|            |                |            |                  |                   |
|            | greater than   | >          | ``expr > expr``  | left              |
+            +----------------+------------+------------------+-------------------+
|            | is equal       | ==         | ``expr == expr`` | left              |
|            |                |            |                  |                   |
|            | is not equal   | !=         | ``expr != expr`` | left              |
+------------+----------------+------------+------------------+-------------------+

Binary Operations on Vectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Binary oprations between vectors require extra specification.

#. All binary operations are performed element-wise. This means that the
   specified operation is applied to elements at the same index in both
   vectors with the result then being placed into the same index in the
   result vector. For example:

   ::

            vector v = 1..5 + 1..5;
            print(v);

   prints the following:

   ::

            [2 4 6 8 10]

#. Binary operations *can* be performed between vectors of different
   sizes. For most operations the smaller vector is padded with zeroes
   to match the larger vectors size and then the operation is applied.
   For example:

   ::

            print(6..10 + 1..3);
            print(1..3 + 6..10);

   prints the following:

   ::

            [7 9 11 9 10]
            [7 9 11 9 10]

   The only exception is when the smaller vector is a *divisor*. A
   divisor must be extended with ones to prevent division by zero
   errors. For example:

   ::

            print(6..10 / 1..3);
            print(6..8 / 1..5);

   prints the following:

   ::

            [6 3 2 9 10]
            [6 3 2 0 0]

#. Boolean operators between vectors are still applied element-wise, but
   the result will be converted to an integer as decribed in *SCalc*
   before being saved into the result. For example:

   ::

            vector a = [i in 0..5 | i / 2];
            vector b = [i in 1..6 | i / 2];
            print(a);
            print(b);
            print(a == b);

   prints the following:

   ::

            [0 0 1 1 2 2]
            [0 1 1 2 2 3]
            [1 0 1 0 1 0]

Integer to Vector Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integers used in expressions with vectors will be promoted to vectors.
The scalar value will be copied into *each index* of a new vector the
same size as the other operand before applying the operator in the
regular vector fashion. For example:

::

     print(1..5 + 5);
     print(2 * 3..6);
     print(5 < 3..7);

prints the following:

::

      [6 7 8 9 10]
      [6 8 10 12]
      [0 0 0 1 1]

A more complicated example:

::

     print(5 + [i in 1..3 | 0] + 1..5);

prints the following:

::

     [6 7 8 4 5]

One might expect:

::

     [6 7 8 9 10]

but recall that addition is left associative. Therefore the order of the
operations in the print statement is:

::

     print((5 + [i in 1..3 | 0]) + 1..5);

The five will be promoted to a vector of length three to match the
generator, resulting in ``[5 5 5]``, which will be added to the
generator for no change. Then it will be *extended* to match the length
five range as ``[5 5 5 0 0]`` before being added to create the final
result of ``[6 7 8 4 5]``.

Vector Indexing
~~~~~~~~~~~~~~~

Vectors can be indexed by a scalar to produce the integer value at a
specified index. Vectors in *VCalc* are *zero indexed*. As well,
indexing outside of the bounds of a vector (e.g. ``v[i]`` where
:math:`0 <= |v| < l` and :math:`i < 0` or :math:`i >= l`) is *not an
error*. An index out of bounds *always returns zero*.

Index domains must be vectors:

-  Domain can be an identifier for a vector.

-  Domain can be the result of a range, generator, filter, or another
   index expression with a vector index (see below).

-  Domain cannot be an integer. For example, this is invalid:

   ::

            print(1[1]);

Examples of valid index expressions:

::

     vector v = 1..5;
     print(v[0 - 1]);
     print(v[2]);
     print(v[5]);
     print([i in v | i * 2][3]);
     print([i in v & i > 2][0]);

prints the following:

::

     0
     3
     0
     8
     3

Domain vectors can also be indexed by a domain indexing vector to
produce a new result vector. This new vector will contain the values of
the domain vector as if each of the values in the domain indexing vector
had individually indexed the domain vector and then been appended to the
result vector. For example:

::

     vector v = 1..7;
     vector i = 2..4;
     print(v[i]);
     print(v[i * 2]);

prints the following:

::

     [3 4 5]
     [5 7 0]

Each value in ``i`` serves as an index into ``v``. Each value indexed
from v is appended to the result and then printed.

