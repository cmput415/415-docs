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
3.  Constructors for aggregate types, provided they follow the rules below.
4.  Index or field access on ``constexpr`` aggregate types.
5.  Other variables that are themselves valid ``constexpr``s.

An expression is **not** a ``constexpr`` if it contains:

1.  References to ``var`` variables.
2.  Function or procedure calls.
3.  Any I/O operations (``<-``).

The compiler must perform this validation recursively. When checking if a variable
is a ``constexpr``, the compiler must trace its entire dependency chain. If the
chain ever depends on a runtime value, the check fails.

**Examples:**

::

    // Legal Constant Expressions
    const A = 10;
    const B = A * 2; // Depends on another constexpr
    const C = B + 5; // C is 25

    // Illegal Constant Expressions
    var x = 10;
    const Y = x + 5; // Illegal: depends on a 'var'

    function get_val() returns integer { return 100; }
    const Z = get_val(); // Illegal: depends on a function call

.. _ssec:constexpr_aggregates:

Constant Expressions with Aggregate Types
-----------------------------------------

Arrays and tuples can also be ``constexpr``s if they meet specific criteria,
allowing them to be used to define other constants.

#. Arrays

   A ``const`` statically-sized array is a ``constexpr`` if:
   1. Its size is a valid ``constexpr``.
   2. All of its element initializers are valid ``constexpr``s.

   Dynamically-sized arrays (e.g., ``integer[*]``) cannot be ``constexpr``
   aggregates as their size is not known at compile time.

   ::

        const WIDTH = 5;
        const LOOKUP_TABLE: integer[WIDTH] = [10, 20, 30, 40, 50]; // Legal constexpr array

        const ELEMENT = LOOKUP_TABLE[3]; // Legal: ELEMENT is a constexpr with value 30
        var my_array: integer[ELEMENT];  // Legal: creates a static array of size 30

        const BAD_TABLE: integer[2] = [10, get_val()]; // Illegal: initializer is not a constexpr


   Note that these rules also apply to variables marked ``const`` within
   non-global scopes.

#. Tuples

   A ``const`` tuple is a ``constexpr`` if all of its fields are initialized with
   valid constant expressions.

   ::

        const CONFIG = (true, 10 * 2); // Legal constexpr tuple

        const IS_ENABLED = CONFIG.1; // Legal: IS_ENABLED is a constexpr with value 'true'
        const VALUE = CONFIG.2;      // Legal: VALUE is a constexpr with value 20
