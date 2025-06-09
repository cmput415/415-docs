.. _sec:expressions:

Expressions
===========

Expressions can only exist within a statement or another expression.

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

A generator may be used to construct either a one or two dimensional array.
A generator creates a value of a 1D array type when one domain variable is
used, and a 2D array type when two domain variables are used.
Any other number of domain variables will yield an error.

A generator consists of either one or two domain expressions,
and an additional  expression on the right hand side of the bar (``|``).
This additional expression is used to create the generated values. For example:

::

         integer[10] v = [i in 1..10 | i * i];
         /* v[i] == i * i */

         integer[2][3] M = [i in 1..2, j in 1..3 | i * j];
         /* M[i][j] == i * j */

The expression to the right of the bar (``|``), is used to generate the
value at the given index.
Let ``T`` be the type of the expression to the right of the bar (``|``). Then,
if the domain of the generator is an array of size ``N``, the result will be a
array of size ``N`` with element type ``T``. Otherwise, if the domain of the
generator is a matrix of size ``N`` x ``M``, the result will be a matrix of size
``N`` x ``M`` with element type ``T``.
Generators may be nested, and
may be used within domain expressions. For instance, the generator below
is perfectly legal:

::

         integer i = 7;

         /* The domain expression should use the previously defined i \*/
         integer[*] v = [i in [i in 1..i | i] | [i in 1..10 | i * i][i]];

         /* v should contain the first 7 squares. */

.. _ssec:expressions_dom_expr:

Domain Expressions
------------------

Domain expressions consist of an identifier denoting an iterator variable and
an expression that evaluates to **any** array type.
Domain expressions can only appear within iterator loops and generators.
A domain expression is a way of declaring a variable that
is local to the loop or generator, that takes on values from
the domain expression array in order.
Domain expressions must evaluate to a type, which means empty literal arrays
yield a ``TypeError``.
The scope of the domain variables (the left hand side of the declaration) is
within the body of the generator or loop.
The domain expressions (the right hand side) are all evaluated before any of the
domain variables are initialized, and therefore the domain expression scope is
the one enclosing the iterator loop or generator.

For instance:

::

         integer i = 7;

         /* This will print 1234567 */
         loop i in 1..i {
           i -> std_output;
         }

Domain variables are not initialized when they are declared. For
instance, in loops they are initialized at the start of each execution of
the loop’s body statement. However, we may chain domain variables using
commas, such as in matrix generators.

::

         integer i = 2;

         /* The "i"s both domain expressions are at the same scope, which is
          * the one enclosing the loop. Therefore the matrix is: [[0 0 0] [0 1 2] [0 2 4]]
          */
         integer[3,3] = [ i in 0..i, j in 0..i | i*j ];

The domain for the domain expression is only evaluated once. For
instance:

::

         integer x = 1;

         /* 1..x is only evaluated the first time the loop executes, so it is
            simply 1..1, and not an infinite loop. */
         loop i in 1..x {
           x = x + 1;
         }

This is true for domain expressions within generators as well.

Iterator variables can be assigned to and re-declared within the enclosed iterator loop.
The variable is re-initialized according to the expression each iteration.

::

         loop i in 1..6 {
           integer i = 5;
         }   
