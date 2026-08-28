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
| (Lowest) 12    | ``||``                             | right             |
+----------------+------------------------------------+-------------------+

The stream operators ``->`` and ``<-`` are statement-level operators, not
expression operators, so they do not appear in the table above. They bind more
loosely than every operator listed, being effectively the very bottom of the
precedence relation. An entire expression is evaluated before it is sent
to or read from a stream (see :ref:`sec:streams`).

.. _ssec:expressions_generators:

Generators
----------

A generator may be used to construct either a one or two dimensional array.
A generator always yields an :ref:`array <ssec:array>` value
whose size is settled at the moment the
generator is evaluated and is fixed thereafter.
A generator creates a value of a 1D array type when one
:term:`iterator variable` is used, and a 2D array type when two
iterator variables are used.
Supplying any other number of iterator variables is :term:`ill-formed`: the
compiler must emit a ``SyntaxError`` (see :ref:`sec:errors`).
Higher-dimensional generators are a potential addition to a future
revision of this specification.

The :term:`domain` in a domain expression is any array-typed value:
static arrays, dynamically-sized :ref:`vectors <ssec:vector>`,
:ref:`strings <ssec:string>`, and :ref:`ranges <sssec:array_ops>`
all count.

A generator consists of either one or two
:term:`domain expressions <domain expression>`, and an additional
expression on the right hand side of the bar (``|``).
This additional expression is used to create the generated values. For example:

::

         integer[10] v = [i in 1..10 | i * i];
         /* v[i] == i * i */

         integer[2][3] M = [i in 1..2, j in 1..3 | i * j];
         /* M[i][j] == i * j */

The expression to the right of the bar (``|``) is used to generate the
value at the given index.

Let ``T`` be the type of the expression to the right of the bar (``|``).
With one iterator variable ranging over a domain of size
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
denoting an :term:`iterator variable` and an expression
that evaluates to an array type.
Domain expressions can only appear within
:ref:`iterator loops <sssec:statements_iter_loop>` and generators.
A domain expression is a way of declaring a variable that is local to
the loop or generator, that takes on values from the domain in order.
The domain's element type must be inferable, so an empty array literal
yields a ``TypeError``.
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

Iterator variables are initialized after their domain. In
loops, :term:`re-initialization` happens at the start of each
execution of the loop's body statement. Only generators
may chain iterator variables
using commas.

::

         integer i = 2;

         /* The "i"s in both domain expressions are at the same scope, which is
          * the one enclosing the generator. Therefore the matrix is: [[0 0 0] [0 1 2] [0 2 4]]
          */
         integer[3][3] mat = [ i in 0..i, j in 0..i | i*j ];

The domain of a domain expression is only evaluated once. For
instance:

::

         integer x = 2;

         /* 1..x is evaluated once, when control first reaches the loop, so it
            is simply 1..2 -- the two-element range [1, 2] -- and not an infinite
            loop. */
         loop i in 1..x {
           x = x + 1;
         }

This is true for domain expressions within generators as well.

Because the domain is captured by evaluating it once, a runtime-sized
domain fixes its iteration count at :term:`initialization`. A :ref:`vector
<ssec:vector>` or :ref:`string <ssec:string>` may serve as the domain; the
length it holds at the moment the domain is captured fixes the number of
iterations, before the loop body executes.

A range domain may be empty. Because ``i..j`` has length ``max(0, j - i + 1)``
(see :ref:`sssec:array_ops`), a domain such as ``5..1`` is the empty range, so a
loop or generator over it simply iterates zero times, equivalent to using
the empty array literal ``[]``:

::

         loop i in 5..1 { i -> std_output; } /* 5..1 is empty: body runs 0 times */

Iterator variables can be assigned to and :term:`re-declared
<re-declaration>` within the enclosed iterator loop. Neither carries
information into the next iteration: the next iteration performs
:term:`re-initialization` from the captured domain, so any shadowing
binding introduced by :term:`re-declaration` is torn down and the
iterator variable is bound fresh.

::

         loop i in 1..6 {
           i -> std_output; // produces 123456
           integer i = 5;
         }

         loop i in 1..6 {
           integer i = 5;
           i -> std_output; // produces 555555
         }

