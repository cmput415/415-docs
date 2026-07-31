.. _sec:global:

Globals
=======

Valid global scope statements inclulde: 

* Variable Declarations
* Struct Declarations
* Function and Procedure Declarations
* Function and Procedure Prototypes
* Typealias

All global statements are considered declarations. Global statements may occur
in any order, given respective symbols are defined before being referenced.

Variable Declarations
---------------------

In *Gazprea* values can be assigned to a global identifier. All globals
must be immutable (``const``). If a global identifier is declared with
the ``var`` specifier, then an error should be raised. This restriction is in
place since mutable global variables would ruin functional purity.
If functions have access to mutable global state then we can not guarantee
their purity.

Globals must be initialized, but the initialization expressions may only contain
a single _scalar_ literal. That means that functions and even previously defined globals may not
appear on the RHS of a global declaration. The reason is because it is very difficult to
evaluate variables and functions at compile time. Global expression evaluation could
be deferred to runtime, but that has the disadvantage of changing errors from compile
time to run time.

For the same reason, a global :ref:`array <ssec:array>` must state its size
explicitly, and that size expression is subject to the same restriction as a
:ref:`typealias <sec:typealias>` size: it must be composed exclusively of
arithmetic on scalar literals, so that the array's length is settled at compile
time rather than at some runtime elaboration point. An inferred size (``[*]``)
is not available at global scope, because the scalar literal on the RHS carries
no length to infer from.

::

  const integer[4] g = 0;      /* legal -- [0, 0, 0, 0] */
  const integer[2 + 2] h = 1;  /* legal -- constant folded to 4 */
  const integer[*] i = 0;      /* illegal -- nothing to infer a length from */


