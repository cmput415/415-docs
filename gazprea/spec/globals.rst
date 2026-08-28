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
Global statements must be written in **dependency order**, and this is a hard
requirement: a global may reference only symbols already defined *earlier* in
the file, so globals are initialized in the order they are written. A global
whose initializer references a global not yet defined at that point is
:term:`ill-formed` and the
compiler must emit a ``SymbolError`` (see :ref:`sec:errors`).

Only global variable initializers are required to be written in dependency
order. References between
functions and procedures are not bound by textual order. Consult 
:ref:`prototype <ssec:function_fwd_declr>` for forward declaration
rules in functions

A statement other than a declaration at global scope must emit a
``GlobalError`` (see
:ref:`sec:errors`). An
assignment that targets a global from within a routine body instead an
``AssignError`` (see :ref:`sec:errors`), as every global is ``const``
(see below).

Variable Declarations
---------------------

In *Gazprea* values can be assigned to a global :term:`identifier`. All
globals must be immutable (``const``). If a global identifier is declared
with the ``var`` specifier, then the compiler must emit a ``GlobalError``
(see :ref:`sec:errors`). This restriction is in place since mutable global
variables would make :term:`functional purity` undecidable in general.

Globals must always be initialized with a valid
:ref:`constant expression <sec:constexpr>`. Unlike a local variable, a global is
never implicitly :term:`zero-initialized <zero value>`: a global declared
without an initializer is :term:`ill-formed`, and the compiler must emit a
``GlobalError`` (see :ref:`sec:errors`). If a zero-value is intended it 
must be written explicitly (for example
``const integer i = 0;`` or ``const integer[3] a = 0;``). A global
:term:`initializer` may reference other globals and use arithmetic and constexpr
aggregates, but it must be fully evaluable by the compiler before the
program runs. As a consequence:

*   Functions, procedures, and I/O operations may not appear in a global's
    initializer.
*   A global ``vector`` or ``string`` is permitted only when it is ``const``
    with a ``constexpr`` initializer, its length is fixed at
    compile time, so a ``const`` vector is equivalent to an array the size of
    its initializer. Consequently ``const string s = "hi";`` and
    ``const vector<integer> v = [1, 2, 3];`` are legal globals. 
    An inferred-size array such as
    ``const integer[*] X = [1, 2, 3]`` is likewise permitted if the initializer
    is a constexpr (see :ref:`sssec:array_sizing`).

The compiler must emit a ``GlobalError`` (see :ref:`sec:errors`) for any
violation of the above rules.

*   **lemma**: All globals are ``constexpr``.
