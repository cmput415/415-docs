.. _sec:expressions:

Expressions
===========

:term:`Expressions <expression>` can only exist within a :term:`statement`
or another expression.

.. _ssec:expressions_toop:

Table of Operator Precedence
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
| 3              | ``^``                              | right             |
+----------------+------------------------------------+-------------------+
| 4              | unary ``+``, unary ``-``, ``not``  | right             |
+----------------+------------------------------------+-------------------+
| 5              | ``*``\ , ``/``\ , ``%``, ``**``    | left              |
+----------------+------------------------------------+-------------------+
| 6              | ``+``\ , ``-``                     | left              |
+----------------+------------------------------------+-------------------+
| 7              | ``..``                             | N/A               |
+----------------+------------------------------------+-------------------+
| 8              | ``<``\ , ``>``\ , ``<=``\ , ``>=`` | left              |
+----------------+------------------------------------+-------------------+
| 9              | ``==``\ , ``!=``                   | left              |
+----------------+------------------------------------+-------------------+
| 10             | ``and``                            | left              |
+----------------+------------------------------------+-------------------+
| 11             | ``or``\ , ``xor``                  | left              |
+----------------+------------------------------------+-------------------+
| (Lowest) 12    | ``||``                             | left              |
+----------------+------------------------------------+-------------------+

The stream operators ``->`` and ``<-`` are statement-level operators, not
expression operators, so they do not appear in the table above. They bind more
loosely than every operator listed -- effectively the very bottom of the
precedence relation -- so an entire expression is evaluated before it is sent
to or read from a stream (see :ref:`sec:streams`).

Two consequences of this table are worth calling out, because both changed
how computed ranges parse:

- Unary ``+``/``-``/``not`` (precedence 4) bind *looser* than exponentiation
  ``^`` (precedence 3), so ``-2^2`` parses as ``-(2^2) = -4`` (as in ordinary
  mathematics), not ``(-2)^2``.

- The range operator ``..`` (precedence 7) binds *looser* than every unary and
  arithmetic operator, so ``-4..5`` parses as ``(-4)..5`` and ``1..n-1`` parses
  as ``1..(n-1)`` -- the bounds are computed first, then the range is formed.

The indexing operator ``[]`` (precedence 2) is a *postfix, multi-axis* operator:
a maximal run of subscripts written directly against an array operand --
``a[s1][s2]...[sk]`` -- is a single :ref:`positional index <sssec:array_slices>`
on that operand, with ``sm`` selecting along axis ``m`` (see :ref:`ssec:matrix`).
Its left-associativity only fixes the order in which the axes are read (left to
right, outermost axis first); it does **not** re-index an intermediate result.
Because the axes are counted against the operand, parentheses matter:
``M[1..3][2]`` indexes ``M`` positionally and selects column 2 of rows 1--2,
whereas ``(M[1..3])[2]`` first evaluates ``M[1..3]`` to an array value and then
indexes *that* value on its own first axis (selecting a row). Parenthesizing an
inner slice -- or binding it to a variable -- is therefore how one indexes into
a slice's result.

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
Supplying any other number of iterator variables is :term:`ill-formed` and is
reported through *Gazprea*'s standard error taxonomy rather than as a
generator-specific error: the compiler must emit a ``SyntaxError`` (see
:ref:`sec:errors`).
In particular, *Gazprea* does not currently support generators over
three or more iterator variables (no direct construction of arrays
with three or more dimensions).

The :term:`domain` in a domain expression is any array-typed value:
static arrays, dynamically-sized :ref:`vectors <ssec:vector>`,
:ref:`strings <ssec:string>`, and :ref:`ranges <sssec:array_ops>`
all count.  The generator
dimension is determined solely by how many iterator variables the
generator introduces (one or two), not by the shape of the domain
value.

A generator consists of either one or two
:term:`domain expressions <domain expression>`, and an additional
expression on the right hand side of the bar (``|``).
This additional expression is used to create the generated values. For example:

::

         integer[10] v = [i in 1..11 | i * i];
         /* v[i] == i * i */

         integer[2][3] M = [i in 1..3, j in 1..4 | i * j];
         /* M[i][j] == i * j */

The expression to the right of the bar (``|``) is used to generate the
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
         integer[*] v = [i in [i in 1..i+1 | i] | [i in 1..11 | i * i][i]];

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
         loop i in 1..i+1 {
           i -> std_output;
         }

Iterator variables are not initialized when they are declared. In
loops, :term:`re-initialization` happens at the start of each
execution of the loop's body statement. A generator -- but not an
iterator loop, which permits only a single domain expression (see
:ref:`sssec:statements_iter_loop`) -- may chain iterator variables
using commas, such as in matrix generators.

::

         integer i = 2;

         /* The "i"s both domain expressions are at the same scope, which is
          * the one enclosing the generator. Therefore the matrix is: [[0 0 0] [0 1 2] [0 2 4]]
          */
         integer[3][3] mat = [ i in 0..i+1, j in 0..i+1 | i*j ];

The domain of a domain expression is only evaluated once. For
instance:

::

         integer x = 2;

         /* 1..x is only evaluated the first time the loop executes, so it is
            simply 1..2 -- the one-element range [1] -- and not an infinite
            loop. */
         loop i in 1..x {
           x = x + 1;
         }

This is true for domain expressions within generators as well.

Because the domain is captured by evaluating it once, a runtime-sized
domain fixes its iteration count at :term:`initialization`. A :ref:`vector
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
