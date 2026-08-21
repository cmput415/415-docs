.. _sec:expressions:

Expressions
===========

:term:`Expressions <expression>` can only exist within a :term:`statement`
or another expression.

.. _ssec:expressions_toop:

Table of Operator precedence
----------------------------

The following is a table containing all of the precedences and
associativities of the operators in *Gazprea*. Parentheses are not
listed: they do not participate in the precedence relation and instead
override it by grouping their contents into a new atom.

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
| 8              | ``<``\ , ``>``\ , ``<=``\ , ``>=`` | left              |
+----------------+------------------------------------+-------------------+
| 9              | ``==``\ , ``!=``                   | left              |
+----------------+------------------------------------+-------------------+
| 10             | ``and``                            | left              |
+----------------+------------------------------------+-------------------+
| 11             | ``or``\ , ``xor``                  | left              |
+----------------+------------------------------------+-------------------+
| (Lowest) 12    | ``||``                             | right             |
+----------------+------------------------------------+-------------------+

.. _ssec:expressions_generators:

Generators
----------

A generator may be used to construct either a one or two dimensional array.
A generator always yields an :ref:`array <ssec:array>` value -- never a
:ref:`vector <ssec:vector>` -- whose size is settled at the moment the
generator is evaluated and is fixed thereafter. Using a generator (or a
range) to initialize an inferred-size array such as an ``integer[*]`` is
therefore one of the ways an array's length becomes fixed at
:term:`initialization` (see :ref:`sssec:array_sizing`).
A generator creates a value of a 1D array type when one
:term:`iterator variable` is used, and a 2D array type when two
iterator variables are used.
Supplying any other number of iterator variables is ill-formed and is
reported through *Gazprea*'s standard error taxonomy rather than as a
generator-specific error: the compiler must emit a ``SyntaxError`` (see
:ref:`sec:errors`).
In particular, *Gazprea* does not currently support generators over
three or more iterator variables (no direct construction of arrays
with three or more dimensions).

The :term:`domain` in a domain expression is any array-typed value:
static arrays, dynamically-sized :ref:`vectors <ssec:vector>`, and
:ref:`ranges <ssec:expressions_toop>` all count.  The generator
dimension is determined solely by how many iterator variables the
generator introduces (one or two), not by the shape of the domain
value.

A generator consists of either one or two
:term:`domain expressions <domain expression>`, and an additional
expression on the right hand side of the bar (``|``).
This additional expression is used to create the generated values. For example:

::

         integer[10] v = [i in 1..10 | i * i];
         /* v[i] == i * i */

         integer[2][3] M = [i in 1..2, j in 1..3 | i * j];
         /* M[i][j] == i * j */

The expression to the right of the bar (``|``), is used to generate the
value at the given index.
Let ``T`` be the type of the expression to the right of the bar (``|``). The
rank of the result is fixed by the number of iterator variables, not by the
shape of any domain. With one iterator variable ranging over a domain of size
``N``, the result is a 1D array of size ``N`` with element type ``T``. With two
iterator variables ranging over domains of size ``N`` and ``M`` respectively,
the result is a 2D array of size ``N`` x ``M`` with element type ``T``.
Generators may be nested, and
may be used within domain expressions. For instance, the generator below
is perfectly legal:

::

         integer i = 7;

         /* The domain expression should use the previously defined i */
         integer[*] v = [i in [i in 1..i | i] | [i in 1..10 | i * i][i]];

         /* v should contain the first 7 squares. */

.. _ssec:expressions_dom_expr:

Domain Expressions
------------------

A :term:`domain expression` consists of an :term:`identifier`
denoting an :term:`iterator variable` and an expression -- the
:term:`domain` -- that evaluates to **any** array type.
Domain expressions can only appear within
:ref:`iterator loops <sssec:statements_iter_loop>` and generators.
A domain expression is a way of declaring a variable that is local to
the loop or generator, that takes on values from the domain in order.
The domain's element type must be inferable, so an empty array literal --
which has no inferable element type -- yields a ``TypeError``.
The :term:`scope` of the iterator variable (the left hand side of the
declaration) is within the body of the generator or loop.
The domain (the right hand side) is evaluated before any of the
iterator variables are initialized, and therefore the scope of the
domain is the one enclosing the iterator loop or generator.

For instance:

::

         integer i = 7;

         /* This will print 1234567 */
         loop i in 1..i {
           i -> std_output;
         }

Iterator variables are not initialized when they are declared. In
loops, :term:`re-initialization` happens at the start of each
execution of the loop's body statement. We may chain iterator
variables using commas, such as in matrix generators.

::

         integer i = 2;

         /* The "i"s both domain expressions are at the same scope, which is
          * the one enclosing the loop. Therefore the matrix is: [[0 0 0] [0 1 2] [0 2 4]]
          */
         integer[3][3] mat = [ i in 0..i, j in 0..i | i*j ];

The domain of a domain expression is only evaluated once. For
instance:

::

         integer x = 1;

         /* 1..x is only evaluated the first time the loop executes, so it is
            simply 1..1, and not an infinite loop. */
         loop i in 1..x {
           x = x + 1;
         }

This is true for domain expressions within generators as well.

Because the domain is captured by evaluating it once, a runtime-sized
domain fixes its iteration count at that moment. A :ref:`vector
<ssec:vector>` or :ref:`string <ssec:string>` may serve as the domain,
and the length it holds when the domain is evaluated sets the number of
iterations; growing the vector or string inside the loop body does not
add iterations.

Iterator variables can be assigned to and :term:`re-declared
<re-declaration>` within the enclosed iterator loop.  Neither carries
information into the next iteration: the next iteration performs
:term:`re-initialization` from the captured domain, so any shadowing
binding introduced by :term:`re-declaration` is torn down and the
iterator variable is bound fresh.

::

         loop i in 1..6 {
           integer i = 5;
         }   
