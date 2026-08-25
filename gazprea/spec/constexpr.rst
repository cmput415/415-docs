.. _sec:constexpr:

Constant Expressions
====================

A :term:`constant expression` (sometimes called a constexpr) is an
:term:`expression` that can be fully evaluated by the :term:`compiler` at
:term:`compile time`. This feature is primarily
for specifying the size of
:ref:`statically-sized arrays <ssec:array>`.

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

An expression is **not** a ``constexpr`` if it contains:

1.  References to ``var`` variables.
2.  Function or procedure calls.
3.  Any I/O operations (``<-``).

The compiler must perform this validation recursively. When checking if a
variable is a ``constexpr``, the compiler must trace its entire dependency
chain. If the chain ever depends on a :term:`run time` value, the check
fails.

A context that requires a ``constexpr`` -- a global initializer (see
:ref:`sec:global`) or a ``typealias`` size (see :ref:`sec:typealias`) -- reports
that context's own error when this check fails: a ``GlobalError`` for a global.
For a ``typealias`` size the specification does not mandate a specific error, and
the test battery is permissive here -- an implementation that accepts a
non-``constexpr`` size, or diagnoses it late, is not penalized.

The only expressions that *must* be ``constexpr`` are global constants and
the size expressions used to parameterize a ``typealias`` (see
:ref:`sec:typealias`). Other constexprs arising from constants inside
function :term:`scope` may also be constexprs
but the implementation does not need to enforce or necessarily identify this.
Students should also note that MLIR has a constant propagation pass built-in,
so doing constant folding yourself may not be necessary depending on your
implementation.

**Examples:**

**Note**: we will annotate the scope explicitly in these examples. Some
'illegal' examples here would be legal within a non-global scope.

::

    // ----------------------------
    // in global scope
    // ----------------------------

    // Legal Global Constant Expressions
    const A = 10;
    const B = A * 2; // Depends on another constexpr
    const C = B + 5; // C is 25

    // Illegal Global Constant Expressions
    function get_val() returns integer { return 100; }
    const Z = get_val(); // Not a constexpr: depends on a function call

.. _ssec:constexpr_aggregates:

Constant Expressions with Aggregate Types
-----------------------------------------

Arrays and tuples can also be ``constexpr``\ s if they meet specific criteria,
allowing them to be used to define other constants.

#. Arrays

   A ``const`` array is a ``constexpr`` if:

   1. Its size is a valid ``constexpr``.
   2. All of its element initializers are valid ``constexpr``\ s.

   A ``var`` ``vector`` can never be a ``constexpr`` aggregate, since its
   length can change at run time. A ``const`` vector, however, cannot grow --
   its mutating methods (``push``/``append``) require a ``var`` receiver -- so
   a ``const`` vector whose initializer is itself a ``constexpr`` *is* a
   ``constexpr``, equivalent to a ``const`` array whose length is that of its
   initializer (or the empty array, if the ``const`` vector is declared without
   an initializer). Because
   ``string`` is a strong-equivalence alias for ``vector<character>`` (see
   :ref:`ssec:string`), the same holds for ``string``: for example
   ``const vector<integer> v = [1, 2, 3];`` and ``const string s = "hi";`` are
   ``constexpr``\ s. An inferred-size array such
   as ``integer[*] X = [1, 2, 3]`` is a ``constexpr`` when its initializer
   is; ``[*]`` denotes a size inferred once, at :term:`initialization`, not
   a resizable one (see :ref:`sssec:array_sizing`). An array whose size or
   initializer is only known at run time is still a perfectly legal array
   -- it is simply not a ``constexpr``.

   ::

        // ----------------------------
        // in global scope
        // ----------------------------

        const WIDTH = 5;
        const integer[WIDTH] LOOKUP_TABLE = [10, 20, 30, 40, 50]; // Legal constexpr array

        const ELEMENT = LOOKUP_TABLE[3];          // Legal: ELEMENT is a constexpr with value 30
        integer[ELEMENT] my_array = 0;            // Legal: static array of size 30, zero-filled

        const integer[2] BAD_TABLE = [10, get_val()]; // Illegal: initializer is not a constexpr

   This would remain illegal even if ``get_val()`` were a procedure: a call
   may appear only as the direct right-hand side of a declaration or
   assignment, or as the callee of a ``call`` statement, and its result may
   not be used in the direct construction of a differently-typed aggregate
   (see :ref:`procedure call positions <ssec:procedure_call_positions>`);
   here the call is nested inside the array literal, not the declaration's
   direct right-hand side.

   A ``constexpr`` can appear anywhere a ``const`` declaration is legal,
   including inside functions, procedures, and control-flow blocks. However,
   **not every** ``const`` variable is a ``constexpr``. ``const`` means only
   that the variable is immutable within its scope; ``constexpr`` is the
   stronger property that the value is fully known at :term:`compile time`.
   For example:

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

   The compiler propagates the constexpr property through local scopes
   normally; there is no restriction on where in a block the declaration
   appears, as long as its entire dependency chain satisfies the rules above.

#. Tuples

   A ``const`` tuple is a ``constexpr`` if all of its fields are initialized
   with valid constant expressions.

   ::

        // ----------------------------
        // in global scope
        // ----------------------------
        const CONFIG = (true, 10 * 2); // Legal constexpr tuple

        const IS_ENABLED = CONFIG.1; // Legal: IS_ENABLED is a constexpr with value 'true'
        const VALUE = CONFIG.2;      // Legal: VALUE is a constexpr with value 20
