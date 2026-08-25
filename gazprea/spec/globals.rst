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
Global statements must be written in **dependency order**: any symbol a global
statement references must already be defined earlier in the file. The one
exception is calls to functions and procedures, for which a forward
:ref:`prototype <ssec:function_fwd_declr>` lets a later definition be
referenced before it textually appears.

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

Globals must always be initialized with a valid
:ref:`constant expression <sec:constexpr>`. Unlike a local variable, a global is
never implicitly :term:`zero-initialized <zero value>`: a global declared
without an initializer is :term:`ill-formed`, and the compiler must emit a
``GlobalError`` (see :ref:`sec:errors`). A zero value is never assumed for a
global -- if one is intended it must be written explicitly (for example
``const integer i = 0;`` or ``const integer[3] a = 0;``). A global
:term:`initializer` may reference other globals and use arithmetic and constexpr
aggregates, but it must be fully evaluable by the compiler before the
program runs. This preserves functional purity and enables
:term:`compile-time <compile time>` optimizations. As a consequence:

*   Functions, procedures, and I/O operations may not appear in a global's
    initializer.
*   A global ``vector`` or ``string`` is permitted only when it is ``const``
    with a ``constexpr`` initializer -- which, since every global is already
    ``const`` (see above), is the same requirement placed on every other
    global. Because a ``const`` vector cannot grow (its mutating methods
    ``push``/``append`` require a ``var`` receiver), its length is fixed at
    compile time, so a ``const`` vector is equivalent to an array the size of
    its initializer (or the empty array, when that initializer is the empty
    literal ``[]``). Consequently ``const string s = "hi";`` and
    ``const vector<integer> v = [1, 2, 3];`` are legal globals. (A ``var``
    vector global is still rejected, but for the independent reason that no
    global may be ``var``.) An inferred-size array such as
    ``const integer[*] X = [1, 2, 3]`` is likewise permitted: ``[*]`` denotes
    an inferred size that is fixed by its ``constexpr`` initializer at compile
    time (see :ref:`sssec:array_sizing`).
*   All globals are implicitly ``constexpr``.

The compiler must emit a ``GlobalError`` (see :ref:`sec:errors`) for any
violation of the above.


