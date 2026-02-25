.. _sec:global:

Globals
=======

Valid global scope statements inclulde:

* Variable Declarations
* Function and Procedure Declarations
* Function and Procedure Prototypes
* Typealias

All global statements are considered declarations. Global statements may occur
in any order, given respective symbols are defined before being referenced.

Variable Declarations
=====================

In *Gazprea* values can be assigned to a global identifier. All globals
must be immutable (``const``). If a global identifier is declared with
the ``var`` specifier, then an error should be raised. This restriction is in
place since mutable global variables would ruin functional purity.
If functions have access to mutable global state then we can not guarantee
their purity.

Globals must be initialized with a valid :ref:`constant expression <sec:constexpr>`.

This requirement ensures that the value of every global can be determined by
the compiler before the program runs. This restriction is in place to support
functional purity and enable compile-time optimizations. As a result of this
rule:

*   Functions, procedures, or I/O operations may not appear in a global's
    initializer.
*   Globals cannot have a dynamically-sized array type (e.g., ``integer[*]``),
    as their size cannot be determined at compile time.
*   All globals are implicitly ``constexpr``.


