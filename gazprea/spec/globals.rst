.. _sec:global:

Globals
=======

Valid global scope statements include: 

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

Globals must be initialized with a valid
:ref:`constant expression <sec:constexpr>`. A global initializer may therefore
reference other globals and use arithmetic and constexpr aggregates, but it must
be fully evaluable by the compiler before the program runs. This preserves
functional purity and enables compile-time optimizations. As a consequence:

*   Functions, procedures, and I/O operations may not appear in a global's
    initializer.
*   A global may not have a ``vector`` type (the dynamically-sized type),
    because a vector's size is determined at runtime. An inferred-size array
    such as ``const integer[*] X = [1, 2, 3]`` *is* permitted: ``[*]`` denotes
    an inferred size that is fixed by its ``constexpr`` initializer at compile
    time.
*   All globals are implicitly ``constexpr``.


