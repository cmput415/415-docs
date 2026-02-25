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

.. _ssec:expressions_range:

Range Operator (``..``)
-----------------------

The range operator ``..`` produces an ``integer[upper - lower]`` array
containing every integer from the lower bound (inclusive) to the upper bound
(exclusive). Both bounds must be ``integer`` expressions; non-integer bounds
are a compile-time type error. Omitting either bound is not supported.

When both bounds are literals or :ref:`constexprs <sec:constexpr>`, the
resulting array type is statically sized. When either bound is a runtime
value, the size is only known at runtime and the result should be stored in
an ``integer[*]`` variable.

::

    integer[4] v = 1..5;   // [1, 2, 3, 4] - size known at compile time
    integer[0] w = 3..3;   // [] - lower equals upper, empty
    integer[0] x = 5..1;   // [] - lower exceeds upper, empty

    var integer n = 10;
    integer[*] y = 1..n;   // size only known at runtime

The result is semantically a deep copy, independent of any variables used to
compute the bounds.

**Special case: inside an indexing expression.**
When ``..`` appears inside square brackets as part of an index operation, it
takes on a different role: it denotes a *slice* of an existing array rather
than producing a standalone integer array. See :ref:`sssec:array_ops` for the
full slicing semantics.

.. _ssec:expressions_stride:

Stride Operator (``by``)
------------------------

The ``by`` operator strides through an array, selecting every *step*-th
element starting from the first, and returns a new independent array whose
elements are deep-copied from the source.

Syntax::

    <array-expr> by <integer-expr>

Given a source array of ``N`` elements and a step ``s``, the result contains
``N / s`` elements (integer division), selecting elements at positions
1, 1+s, 1+2s, and so on.

The step must be a positive ``integer``. If the step expression is a
:ref:`constexpr <sec:constexpr>`, a non-positive value is a compile-time
error; otherwise it is a runtime error.

::

    integer[8] v = 1..9;
    integer[4] a = v by 2;   // [1, 3, 5, 7]
    integer[2] b = v by 3;   // [1, 4]

The ``by`` operator is most commonly combined with ``..`` to produce
arithmetic sequences. When both bounds and the step are literals, all sizes
are statically known:

::

    integer[4] odds  = 1..9 by 2;    // [1, 3, 5, 7]
    integer[4] evens = 2..10 by 2;   // [2, 4, 6, 8]

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

         integer[2, 3] M = [i in 1..2, j in 1..3 | i * j];
         /* M[i, j] == i * j */

The expression to the right of the bar (``|``), is used to generate the
value at the given index.
Let ``T`` be the type of the expression to the right of the bar (``|``). Then,
if the domain of the generator is an array of size ``N``, the result will be a
array of size ``N`` with element type ``T``. Otherwise, if the domain of the
generator is an N-D array of size ``N`` x ``M``, the result will be an array of size
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
         integer[3,3] mat = [ i in 0..i, j in 0..i | i*j ];

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
