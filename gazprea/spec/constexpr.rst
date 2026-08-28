.. _sec:constexpr:

Constant Expressions
====================

A :term:`constant expression` (sometimes called a constexpr) is an
:term:`expression` that can be fully evaluated by the :term:`compiler` at
:term:`compile time`.

In *Gazprea*, a ``constexpr`` is not a keyword, but a property of a ``const``
variable. A ``const`` variable is considered a ``constexpr`` if and only if its
initializer expression meets a strict set of criteria:

.. _ssec:constexpr_rules:

Rules for Constant Expressions
------------------------------

An expression is a valid ``constexpr`` if it is composed exclusively of:

1.  :term:`Literals <literal>` of :term:`primitive types <primitive type>`
    (``boolean``, ``integer``, ``real``, ``character``).
2.  The unary operators ``+``, ``-``, ``not`` applied to a single
    ``constexpr``, and the binary operators ``+``, ``-``, ``*``, ``/``,
    ``%``, ``^``, ``<``, ``>``, ``<=``, ``>=``, ``==``, ``!=``, ``and``,
    ``or``, ``xor`` applied between two ``constexpr``\ s.
3.  Constructors for :term:`aggregate types <aggregate type>`, provided
    that the aggregate is const and all members are ``constexpr``\ s.
4.  Index or field access on ``constexpr`` aggregate types.
5.  Other variables that are themselves valid ``constexpr``\ s.
6.  The implicit :term:`zero value` of a ``const`` declared with no
    initializer (e.g. ``const integer i;`` is the constexpr ``0``).
7.  An aggregate-level operator (element-wise arithmetic, ``**``, ``||``)
    applied between ``constexpr`` aggregates, or a slice of a ``constexpr``
    array; each is itself a ``constexpr`` under these same rules.

A context that requires a ``constexpr`` reports
that context's own error when this check fails, ex. a ``GlobalError``
for a global.

The only expressions that *must* be ``constexpr`` are global constants and
the size expressions used to parameterize a ``typealias`` (see
:ref:`sec:global` and see :ref:`sec:typealias`).
Other constexprs arising from constants inside
function :term:`scope` may also be constexprs
but the implementation does not need to enforce or necessarily identify this.


**Students should also note that MLIR has a constant propagation pass built-in,
so doing constant folding yourself may not be necessary depending on your
implementation.**

**Examples:**

**Note**: we will annotate the scope explicitly in these examples. Some
'illegal' examples here would be legal within a non-global scope.

The legal declarations below form a valid ``constexpr`` chain, so the value
of ``C`` is known at compile time:

.. gazprea-example::
   :name: constexpr_scalar

   // ----------------------------
   // in global scope
   // ----------------------------

   // Legal Global Constant Expressions
   const A = 10;
   const B = A * 2; // Depends on another constexpr
   const C = B + 5; // C is 25

   procedure main() returns integer {
       C -> std_output;
       return 0;
   }

   --- output ---
   25

An initializer that depends on a function call is not a ``constexpr``, so in
global scope the compiler must emit a ``GlobalError`` (see :ref:`sec:errors`):

::

    // ----------------------------
    // in global scope
    // ----------------------------

    // Illegal Global Constant Expressions
    function get_val() returns integer { return 100; }
    const Z = get_val(); // Not a constexpr: depends on a function call

.. _ssec:constexpr_aggregates:

Constant Expressions with Aggregate Types
-----------------------------------------

Arbitrary-rank arrays, tuples and structs can also be ``constexpr``\ s if
they meet
specific criteria,
allowing them to be used to define other constants:
every field or element initializer, and any size, must itself be a
``constexpr``.

An array can be a ``constexpr``, and indexing one yields a ``constexpr``, so
it may size a later declaration:

::

     // ----------------------------
     // in global scope
     // ----------------------------

     const WIDTH = 5;
     const integer[WIDTH] LOOKUP_TABLE = [10, 20, 30, 40, 50]; // Legal constexpr array

     const ELEMENT = LOOKUP_TABLE[3];          // Legal: ELEMENT is a constexpr with value 30
     integer[ELEMENT] my_array = 0;            // Legal: static array of size 30, zero-filled

     const integer[2] BAD_TABLE = [10, get_val()]; // Illegal: initializer is not a constexpr

A ``constexpr`` tuple, and field access on it, are ``constexpr``\ s too:

.. gazprea-example::
   :name: constexpr_tuple

   // ----------------------------
   // in global scope
   // ----------------------------
   const CONFIG = (true, 10 * 2); // Legal constexpr tuple

   const IS_ENABLED = CONFIG.1; // Legal: IS_ENABLED is a constexpr with value 'true'
   const VALUE = CONFIG.2;      // Legal: VALUE is a constexpr with value 20

   procedure main() returns integer {
       IS_ENABLED -> std_output;
       '\n' -> std_output;
       VALUE -> std_output;
       return 0;
   }

   --- output ---
   T
   20

Outside global scope, an immutable ``const`` may take a runtime value; it is
then legal but not a ``constexpr``:

::

     // ----------------------------------
     // in local/function/non-global scope
     // ----------------------------------
     var integer x;
     x <- std_input;
     const integer y = x; // Legal: y is immutable, but NOT a constexpr
                          // because its value depends on runtime input.
     integer[y] arr;      // Legal: the runtime size y is evaluated once,
                          // at initialization, and fixes arr's length for
                          // good; arr is an ordinary (non-constexpr) array
                          // and can never be resized.
     vector<integer> v;   // Legal: use a vector when the collection must
                          // grow or shrink after it is created.

The compiler may propagate the constexpr property through local scopes.
There is no restriction on where in a block the declaration
appears, as long as its entire dependency chain satisfies the rules above.
