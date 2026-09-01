.. _sec:flags:

Flags
=====

*Gazprea* programs are compiled with a fixed set of compiler flags for testing.

.. _ssec:flags_o2:

The -O2 Flag
------------

``-O2`` is a mandatory compiler flag provided **solely for performance
testing**.
Code compiled with ``-O2`` produces exactly the same observable behavior as the
same code compiled without it.

When ``-O2`` is passed, the student compiler must emit code optimized through
LLVM's ``-O2`` optimization pipeline. Every optimization under this flag happens
at the LLVM level:

- Students are **not** required to implement any optimizations of their own.
  Each optimization performed under ``-O2`` is carried out by LLVM; the student
  compiler's only responsibility is to route the flag into that pipeline.
- The project scaffolding already provides this wiring. Accepting ``-O2`` and
  forwarding it to LLVM should therefore require **no substantive changes** to a
  student's compiler.

.. _ssec:flags_testing:

Testing Policy
--------------

Every test is compiled with ``-O2``.
Because ``-O2`` leaves the meaning of a program unchanged, this never alters a
test's expected output; it simply guarantees that the LLVM optimization pipeline
is always exercised.
