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

A ``real`` literal can also be created by any valid ``real`` or ``integer``
literal followed by scientific notation indicated by the character ``e`` or
``E`` and another valid ``integer`` literal. Scientific notation multiplies the
first literal by :math:`{10}^{x}`, e.g. :math:`4.2\mathrm{e}{-3}=4.2
\times10^{-3}`. For example:

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

Real values always use the IEEE 754 representation and semantics for
not-a-number (``NaN``), the signed infinities (``Infinity``), and signed
zeros. Real arithmetic therefore **never** raises a ``MathError``: overflowing
the finite ``real`` range yields a signed ``Infinity``, division or ``%`` by
``0.0`` yields a signed ``Infinity`` (or ``NaN`` for ``0.0 / 0.0``), and every
subsequent operation on ``Infinity`` and ``NaN`` operands follows IEEE 754. The
``-ffast-math`` flag has **no effect** on how ``real`` values are produced or
handled -- in particular it does not change the generation of ``Infinity`` or
``NaN``. (``-ffast-math`` affects only integer arithmetic; see :ref:`sec:flags`
and :ref:`ssec:integer`.)

Comparisons follow from this rule, exactly as in IEEE 754. With at least one
``NaN`` operand, every *affirmative* comparison -- ``==``, ``<``, ``>``,
``<=``, ``>=`` -- evaluates to ``false``, while the *negative* comparison
``!=`` evaluates to ``true``. A ``NaN`` is unordered with respect to every
value, including an ``Infinity`` and including another ``NaN``; so when ``x``
is ``NaN``, ``x == x`` is ``false`` and ``x != x`` is ``true``. Comparisons
that involve only finite values and the infinities behave as ordinary IEEE 754
comparisons; for example ``1.0 / 0.0`` compares greater than every finite
``real``, and ``+Infinity`` compares equal to ``+Infinity``.

Exponentiation (``^``) likewise follows IEEE 754: a negative base raised to a
fractional exponent -- for example ``(-2.0)^0.5`` -- is not a ``MathError`` but
yields ``NaN``.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``real`` may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.
