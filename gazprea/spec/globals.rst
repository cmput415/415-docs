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
Global statements need not be written in dependency order, subject to one
rule: any symbol a global statement references must already be defined
earlier in the file. Function and procedure prototypes lift this rule for
calls, since a prototype lets a later definition be referenced before it
textually appears.

A statement other than a declaration at global scope -- an assignment, an
``if``, a loop, or a bare expression -- must emit a ``GlobalError`` (see
:ref:`sec:errors`).

Variable Declarations
---------------------

In *Gazprea* values can be assigned to a global :term:`identifier`. All
globals must be immutable (``const``). If a global identifier is declared
with the ``var`` specifier, then the compiler must emit a ``GlobalError``
(see :ref:`sec:errors`). This restriction is in place since mutable global
variables would ruin :term:`functional purity`. If functions have access to
mutable global state then the compiler can no longer guarantee their purity.

Globals must be initialized with a valid
:ref:`constant expression <sec:constexpr>`. A global :term:`initializer`
may therefore reference other globals and use arithmetic and constexpr
aggregates, but it must be fully evaluable by the compiler before the
program runs. This preserves functional purity and enables
:term:`compile-time <compile time>` optimizations. As a consequence:

*   Functions, procedures, and I/O operations may not appear in a global's
    initializer.
*   A global may not have a ``vector`` type (the dynamically-sized type),
    because a vector's size is determined at :term:`run time`. Because
    :ref:`string <ssec:string>` is a typealias for ``vector<character>``, a
    global may not have a ``string`` type either (so
    ``const string s = "hi";`` at global scope is a ``GlobalError``). An
    inferred-size array such as ``const integer[*] X = [1, 2, 3]`` *is*
    permitted: ``[*]`` denotes an inferred size that is fixed by its
    ``constexpr`` initializer at compile time
    (see :ref:`sssec:array_sizing`).
*   All globals are implicitly ``constexpr``.

The compiler must emit a ``GlobalError`` (see :ref:`sec:errors`) for any
violation of the above.


