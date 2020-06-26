.. _sec:expressions:

Expressions
===========

.. _ssec:expressions_toop:

Table of Operator precedence
----------------------------

The following is a table containing all of the precedences and
associativities of the operators in *Gazprea*.

+----------------+------------------------------------+-------------------+
| **Precedence** | **Operators**                      | **Associativity** |
+================+====================================+===================+
| (Highest) 1    | ``.``                              | left              |
+----------------+------------------------------------+-------------------+
| 2              | ``[]`` (indexing)                  | left              |
+----------------+------------------------------------+-------------------+
| 3              | ``..``                             | N/A               |
+----------------+------------------------------------+-------------------+
| 4              | unary ``+``, unary ``-``, ``not``  | right             |
+----------------+------------------------------------+-------------------+
| 5              | ``^``                              | right             |
+----------------+------------------------------------+-------------------+
| 6              | ``*``\ , ``/``\ , ``%``, ``**``    | left              |
+----------------+------------------------------------+-------------------+
| 7              | ``+``\ , ``-``                     | left              |
+----------------+------------------------------------+-------------------+
| 8              | ``by``                             | left              |
+----------------+------------------------------------+-------------------+
| 9              | ``<``\ , ``>``\ , ``<=``\ , ``>=`` | left              |
+----------------+------------------------------------+-------------------+
| 10             | ``==``\ , ``!=``                   | left              |
+----------------+------------------------------------+-------------------+
| 11             | ``and``                            | left              |
+----------------+------------------------------------+-------------------+
| 12             | ``or``\ , ``xor``                  | left              |
+----------------+------------------------------------+-------------------+
| (Lowest) 13    | ``||``                             | right             |
+----------------+------------------------------------+-------------------+

.. _ssec:expressions_generators:

Generators
----------

A generator may be used to construct either a vector or a matrix. A
generator creates a value of a vector type when one domain variable is
used, and a generator creates a value of a matrix type when two domain
variables are used. Any other number of domain variables will yield an
error.

A generator consists of either one or two domain expression. An
additional expression is used on the right hand side in order to create
the generated values. For example:

::

         integer vector v[10] = [i in 1..10 | i * i];
         /* v[i] == i * i */

         integer matrix M[2, 3] = [i in 1..2, j in 1..3 | i * j];
         /* M[i, j] == i * j */

The expression to the right of the bar "|", is used to generate the
value at the given index, and must result in a value with the same type
as the base type for the matrix or vector. Generators may be nested, and
may be used within domain expressions. For instance, the generator below
is perfectly legal:

::

         integer i = 7;

         /* The domain expression should use the previously defined i */
         integer vector v = [i in [i in 1..i | i] | [i in 1..10 | i * i][i]];

         /* v should contain the first 7 squares. */

.. _ssec:expressions_filters:

Filters
-------

Filters are used to accumulate elements into vectors. Each filter
contains a single domain expression, and a list of predicates.

The result of a filter operation is a tuple. This tuple contains a field
for each of the predicates in order. Each field is a vector containing
only the elements from the domain which satisfied the predicate
expressions. Each filter result has an additional field which is a
vector containing all of the values in the domain which did not satisfy
any of the predicates. For example:

::

         /* x == ([3], [2], [2, 4], [1, 5]) */
         var x = [i in 1..5 & i == 3 or i == 2 or i % 2 == 0];

         /* y == ([1, 3, 5], [2, 4]) */
         var y = [i in 1..5 & i % 2 == 1);

There must be at least one predicate expression

.. _ssec:expressions_dom_expr:

Domain Expressions
------------------

Domain expressions can only appear within iterator loops, generators,
and filters. A domain expression is a way of declaring a variable that
is local to the loop, generator, or filter, that takes on values from
intervals, and vectors in order.

Domain expressions are essentially declarations, and so they follow the
same scoping rules. For instance:

::

         integer i = 7;

         /* This will print 1234567 */
         loop i in 1..i {
           i -> out;
         }

Domain variables are not initialized when they are declared. For
instance in loops they are initialized at the start of each execution of
the loop’s body statement. However, we may chain domain variables using
commas, like in iterator loops, or matrix generators. Thus it is illegal
to use a domain variable declared in the same chain of domain
expressions, since the value may be uninitialized.

::

         integer i = 7;

         /* This is illegal because the i in "j in 1..i" refers to the domain
            variable i. An error should be raised in this case. */
         loop i in 1..i, j in 1..i {
            i * j -> out;
         }

         /* This is legal since i will be initialized whenever the inner loop
            is executed */
         loop i in 1..i {
           loop j in 1..i {
             i * j -> out;
           }
         }

The domain for the domain expression is only evaluated once. For
instance:

::

         integer x = 1;

         /* 1..x is only evaluated the first time the loop executes, so it is
            simply 1..1, and not an infinite loop. */
         loop i in 1..x {
           x = x + 1;
         }

This is true for domain expressions within generators and filters as
well.
