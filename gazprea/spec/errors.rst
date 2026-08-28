.. _sec:errors:

Errors
======

Every :term:`ill-formed` *Gazprea* program is rejected with an error drawn from
the fixed taxonomy below; a :term:`well-formed` program produces no errors.
This page
is the **normative** source of that taxonomy, the set of error classes and the
condition under which each must be emitted. The *mechanics* of reporting them
(which C++ exception class to throw, the ANTLR error listener, the run-time
error
functions, and how the test harness reads ``stderr``) are up to the
implementation. We provide some guidance in the
:ref:`implementation chapter <sec:errors_impl>`.

Each class is *either* a compile-time or a run-time error, but for several of
them the exact moment of detection is left to the implementation: some
conditions (an out-of-bounds index, a division by zero) are undecidable in
general, so an implementation may catch them at :term:`compile time` when it can
prove them and otherwise at :term:`run time`. The prose throughout this
specification therefore says only that the compiler "must emit" a given error,
naming the *class* rather than the phase at which the compiler should emit the
error.

*Gazprea* Errors
-------------------

The following set of errors are generally classed as compile-time errors in
gazprea.

* ``SyntaxError`` -- the program is not syntactically valid. This covers both
  errors the parser reports directly and *syntactic* errors enforced during
  parsing. The grammar itself need not reject these constructs, but it may.

* ``SymbolError`` -- an undefined symbol is referenced, or a symbol is
  re-defined in the same :term:`scope`.

* ``TypeError`` -- an operation or statement is applied to, or between,
  expressions of invalid or incompatible types. A ``return`` whose value does
  not
  match, and cannot be implicitly cast to, the function or procedure's return
  type is a
  ``TypeError`` (not a ``ReturnError``).

* ``AliasingError`` -- two arguments that may name the same mutable memory are
  passed to a procedure with at least one bound to a ``var`` parameter (see
  :ref:`sec:procedure`). This is always a compile-time diagnosis, using a
  conservative approximation that two values that come from the same array are
  said to alias unconditionally.

* ``AssignError`` -- an assignment whose target is not a ``var`` (an attempt to
  modify a ``const`` value, including assigning to a ``const`` function or
  procedure parameter), a tuple-unpacking assignment whose number of
  :term:`lvalues <lvalue>` differs from the number of fields in the tuple
  :term:`rvalue`, or a scalar initialization of a matrix that has any inferred
  ``[*]`` dimension (which has no shape to infer from the scalar).

* ``MainError`` -- the program has no ``main`` procedure, or ``main`` has an
  :term:`ill-formed` signature (see :ref:`ssec:procedure_main`).

* ``ReturnError`` -- a function or procedure with a return type has a control
  path that reaches its end without a ``return``.

* ``GlobalError`` -- an illegal global: a ``var`` global, a global with no
  initializer or a non-``constexpr`` initializer,
  a global referencing a name not
  yet defined, or a non-declaration statement at global scope (see
  :ref:`sec:global`).

* ``StatementError`` -- the program is syntactically valid but a statement is
  used in an invalid context (for example ``break`` or ``continue`` outside a
  loop).

* ``CallError`` -- ``call`` is applied to a function, a procedure is called in an
  invalid position, or a procedure method is written without ``call``.

* ``DefinitionError`` -- a function or procedure is declared (prototyped) but
  never defined.

* ``LiteralError`` -- a literal does not fit its type (for example an integer
  literal outside the ``i32`` range, or a ``\x`` escape with no
  or too many hex digit(s)).


The following are classified as run-time errors, but an implementation may
instead detect and report them at :term:`compile time` whenever it can prove them
(for instance when the operands are literals); the test harness accepts either
phase.

* ``MathError`` -- an integer math fault: signed 32-bit overflow, division or
  ``%`` by ``0``, or exponentiation of base ``0`` with a non-positive exponent
  (see :ref:`ssec:integer`). ``real`` arithmetic never raises a ``MathError``
  (see :ref:`ssec:real`).

* ``IndexError`` -- an index is out of bounds. For an array this is an integer
  index outside ``1..n`` or ``-n..-1`` (see :ref:`sssec:array_ops`); for a
  :ref:`tuple <ssec:tuple>` it is a field index outside ``1..k`` which -- because
  a tuple index is always a literal -- is necessarily caught at
  :term:`compile time`.

* ``SizeError`` -- an operation or assignment is applied to or between arrays
  whose sizes are invalid or incompatible (see :ref:`sssec:array_sizing`).
