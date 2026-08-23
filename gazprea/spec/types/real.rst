.. _ssec:real:

Real
----

A ``real`` is an IEEE 754 32-bit floating-point value. A ``real`` can be
represented by an ``f32`` in *MLIR*.

.. _sssec:real_decl:

Declaration
~~~~~~~~~~~

A ``real`` value is declared with the keyword ``real``.

.. _sssec:real_lit:

Literals
~~~~~~~~

A ``real`` literal can be specified in several ways. A leading zero is
not necessary and can be inferred from a leading decimal point. Likewise,
a trailing zero is not necessary and can be inferred from a trailing
decimal point. However, at least one digit must be present in order to be
parsed. For example:

::

     42.0
     42.
     4.2
     0.42
     .42
     .  // Illegal.

A ``real`` literal can also be created by any valid ``real`` or
``integer`` literal followed by scientific notation indicated by the
character ``e`` or ``E`` and another valid ``integer`` literal. Scientific notation
multiplies the first literal by :math:`{10}^{x}`, e.g.
:math:`4.2\mathrm{e}{-3}=4.2 \times10^{-3}`. For example:

::

     4.2e-1
     4.2e+9
     4.2E5
     42.e+7
     .42e-7
     42E6

.. _sssec:real_ops:

Operations
~~~~~~~~~~

Floating-point operations are equivalent to :ref:`integer operations
<sssec:integer_ops>`.

The ``%`` operator is defined on ``real`` operands as the decimal
remainder, e.g. ``6.77 % 4.21 == 2.56``.

Under normal evaluation, real arithmetic that overflows the finite ``real``
range, and real division or ``%`` where the right operand is ``0.0``, cause
the implementation to raise a ``MathError`` (see :ref:`sec:errors`). Under the
``-ffast-math`` compiler flag they instead produce the IEEE 754 result -- a
signed ``Infinity``, or ``NaN`` for ``0.0 / 0.0`` -- rather than an error.

Real values use the IEEE 754 representation of not-a-number (NaNs), infinity
(Infs), and zeros.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``real`` may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.
