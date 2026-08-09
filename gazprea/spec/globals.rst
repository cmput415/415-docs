.. _sec:global:

Globals
=======

Valid global :term:`scope` :term:`statements <statement>` include:

* Variable Declarations
* Struct Declarations
* Function and Procedure Declarations
* Function and Procedure Prototypes
* Typealias

All global statements are considered :term:`declarations <declaration>`.
Global statements may occur in any order, given respective symbols are
defined before being referenced.

Variable Declarations
---------------------

In *Gazprea* values can be assigned to a global :term:`identifier`. All
globals must be immutable (``const``). If a global identifier is declared
with the ``var`` specifier, then the compiler must emit a ``GlobalError``
(see :ref:`sec:errors`). This restriction is in place since mutable global
variables would ruin :term:`functional purity`. If functions have access to
mutable global state then we can not guarantee their purity.

Globals must be initialized with a valid
:ref:`constant expression <sec:constexpr>`. A global :term:`initializer`
may therefore reference other globals and use arithmetic and constexpr
aggregates, but it must be fully evaluable by the compiler before the
program runs. This preserves functional purity and enables
:term:`compile-time <compile time>` optimizations. As a consequence:

*   Functions, procedures, and I/O operations may not appear in a global's
    initializer.
*   A global may not have a ``vector`` type (the dynamically-sized type),
    because a vector's size is determined at :term:`run time`. An
    inferred-size array such as ``const integer[*] X = [1, 2, 3]`` *is*
    permitted: ``[*]`` denotes an inferred size that is fixed by its
    ``constexpr`` initializer at compile time.
*   All globals are implicitly ``constexpr``.

The compiler must emit a ``GlobalError`` if any of these restrictions are
violated, including a global that is not initialized, a global with an
initializer that is not a valid constant expression, and a global whose
type is ``vector``.


