.. _sec:constexpr:

Constant Expressions
====================

A constant expression (sometimes called a constexpr) is an expression that can
be fully
evaluated by the compiler at compile time. This feature primarily
for specifying the size of
:ref:`statically-sized arrays <ssec:array>`.

In *Gazprea*, a ``constexpr`` is not a keyword, but a property of a ``const``
variable. A ``const`` variable is considered a ``constexpr`` if and only if its
initializer expression meets a strict set of criteria:

.. _ssec:constexpr_rules:

Rules for Constant Expressions
------------------------------

An expression is a valid ``constexpr`` if it is composed exclusively of:

1.  Literals of base types (``boolean``, ``integer``, ``real``, ``character``).
2.  Operators, including ``+``, ``-``, ``*``, ``/``, ``not``, ``and``, ``or``.
    between two or more ``constexpr``s.
3.  Constructors for aggregate types, provided that the aggregate is const and
    all members are ``constexpr``s.
4.  Index or field access on ``constexpr`` aggregate types.
5.  Other variables that are themselves valid ``constexpr``s.

An expression is **not** a ``constexpr`` if it contains:

1.  References to ``var`` variables.
2.  Function or procedure calls.
3.  Any I/O operations (``<-``).

The compiler must perform this validation recursively. When checking if a variable
is a ``constexpr``, the compiler must trace its entire dependency chain. If the
chain ever depends on a runtime value, the check fails.

The only expressions that *must* be ``constexpr`` are global constants. Other
constexprs arising from constants inside function scope may also be constexprs
but the implementation does not need to enforce or necessarily identify this.
Students should also note that mlir has a constant propagation pass built in,
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
    var x = 10;
    const Y = x + 5; // Not a constexpr: depends on a 'var'

    function get_val() returns integer { return 100; }
    const Z = get_val(); // Not a constexpr: depends on a function call

.. _ssec:constexpr_aggregates:

Constant Expressions with Aggregate Types
-----------------------------------------

Arrays and tuples can also be ``constexpr``s if they meet specific criteria,
allowing them to be used to define other constants.

#. Arrays

   A ``const`` statically-sized array is a ``constexpr`` if:

   1. Its size is a valid ``constexpr``.
   2. All of its element initializers are valid ``constexpr``s.
   3. Any use of the spread operator (``...``) spreads only arrays that are
      themselves ``constexpr``s.

   Dynamically-sized arrays (e.g., ``integer[*]``) cannot be ``constexpr``
   aggregates as their size is not known at compile time.

   ::

        // ----------------------------
        // in global scope
        // ----------------------------

        const WIDTH = 5;
        const integer[WIDTH] LOOKUP_TABLE = [10, 20, 30, 40, 50]; // Legal constexpr array

        const ELEMENT = LOOKUP_TABLE[3];          // Legal: ELEMENT is a constexpr with value 30
        integer[ELEMENT] my_array = 0;            // Legal: static array of size 30, zero-filled

        const integer[2] BAD_TABLE = [10, get_val()]; // Illegal: initializer is not a constexpr
                                                      //  also illegal if a procedure since
                                                      //  procedures calls are not allowed
                                                      //  within declarations

        // Spread of a constexpr array is also a constexpr
        const integer[3] A = [1, 2, 3];
        const integer[5] B = [0, ...A, 4]; // Legal: spread of constexpr A

        // Spread of a non-constexpr array is not
        var integer[*] dyn = [1, 2, 3];
        const integer[5] C = [0, ...dyn, 4]; // Illegal: dyn is not a constexpr


   A ``constexpr`` can appear anywhere a ``const`` declaration is legal,
   including inside functions, procedures, and control-flow blocks. However,
   **not every** ``const`` variable is a ``constexpr``. ``const`` means only
   that the variable is immutable within its scope; ``constexpr`` is the
   stronger property that the value is fully known at compile time. For
   example:

   ::

        // ----------------------------------
        // in local/function/non-global scope
        // ----------------------------------
        var integer x;
        x <- std_input;
        const integer y = x; // Legal: y is immutable, but NOT a constexpr
                             // because its value depends on runtime input.
        integer[y] arr;      // Legal, but not constexpr: y is not a 
                             // constexpr, so it cannot
                             // be used as a static array size. arr is
                             // a dynamic-sized array

   The compiler propagates the constexpr property through local scopes
   normally; there is no restriction on where in a block the declaration
   appears, as long as its entire dependency chain satisfies the rules above.

#. Tuples

   A ``const`` tuple is a ``constexpr`` if all of its fields are initialized with
   valid constant expressions.

   ::

        // ----------------------------
        // in global scope
        // ----------------------------
        const CONFIG = (true, 10 * 2); // Legal constexpr tuple

        const IS_ENABLED = CONFIG.1; // Legal: IS_ENABLED is a constexpr with value 'true'
        const VALUE = CONFIG.2;      // Legal: VALUE is a constexpr with value 20
