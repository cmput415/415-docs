.. _sec:flags:

Flags
=====

*Gazprea* programs are compiled with a fixed set of compiler flags. Almost all
of them leave the meaning of a program unchanged. This page documents the one
flag that changes program semantics -- ``-ffast-math`` -- and states precisely
what it affects and how it may be used.

.. _ssec:flags_ffastmath:

The -ffast-math Flag
--------------------

``-ffast-math`` is a mandatory compiler flag provided **solely for performance
testing**. It is the *single* place in *Gazprea* where a program may exhibit
:term:`undefined behavior`: under standard compilation -- that is, without
``-ffast-math`` -- the language has **no undefined behavior** at all.

Effect on integer arithmetic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Without ``-ffast-math``, the integer operations enumerated in
:ref:`ssec:integer` raise a ``MathError`` (see :ref:`sec:errors`) on a math
fault; :ref:`ssec:integer` is normative for exactly which operations these are.
Under ``-ffast-math`` every one of those faults instead becomes
:term:`undefined behavior` -- no ``MathError`` is raised, and this specification
imposes no requirement whatsoever on the result. The affected faults are:

- signed 32-bit integer overflow of ``+``, ``-``, ``*``, ``/``, ``^``, and unary
  ``-`` (including ``INT_MIN / -1`` and ``-INT_MIN``);
- integer division or remainder ``%`` by ``0``;
- integer exponentiation ``^`` with base ``0`` and a non-positive exponent.

Effect on real arithmetic
~~~~~~~~~~~~~~~~~~~~~~~~~~~

None. ``real`` arithmetic always follows IEEE 754 -- overflow yields a signed
``Infinity``, division or ``%`` by ``0.0`` yields ``Infinity`` or ``NaN``, and
operations on ``Infinity`` and ``NaN`` propagate as usual -- and ``-ffast-math``
never changes this. A ``real`` operation therefore never raises a ``MathError``
and never has undefined behavior, with or without the flag; :ref:`ssec:real` is
normative for real semantics.

.. _ssec:flags_testing:

Testing Policy
--------------

Because ``-ffast-math`` is the only source of undefined behavior, its use in
testing is tightly constrained:

- **Student tests must never exercise undefined behavior.** No student test may
  rely on, or trigger, any of the integer faults listed above.
- ``-ffast-math`` is **reserved for performance testing** -- specifically,
  stress-tests of linear algebra that have already been validated to contain no
  undefined behavior.
- ``-ffast-math`` will **never** exercise undefined behavior in testing. Every
  test is first run against the non-``-ffast-math`` compiler to confirm that it
  contains no undefined behavior *before* it is ever used for performance
  testing under ``-ffast-math``.
