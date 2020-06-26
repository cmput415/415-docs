.. _ssec:real:

Real
----

A ``real`` is an IEEE 754 32-bit floating point value. A ``real`` can be
represented by a ``float`` in *LLVM IR*.

.. _sssec:real_decl:

Declaration
~~~~~~~~~~~

A ``real`` value is declared with the keyword ``real``.

.. _sssec:real_null:

null
~~~~

``null`` is ``0.0`` for ``real``.

.. _sssec:real_ident:

identity
~~~~~~~~

``identity`` is ``1.0`` for ``real``.

.. _sssec:real_lit:

Literals
~~~~~~~~

A ``real`` literal can be specified in several ways. A leading zero is
not necessary and can be inferred from a leading decimal point. For
example:

::

     42.0
     4.2
     42.

A ``real`` literal can also have an attached scientific notation
exponent following the mantissa. Scientific notation multiplies the
literal by :math:`{10}^{x}`. For example, :math:`4.2\mathrm{e}-3=4.2
\times10^{-3}`. The scientific notation can also replace the mantissa
entirely, following immediately after the decimal point. Finally, the
scientific notation can follow just a pure ``integer``, resulting in a
real value. For example:

::

     4.2e-1
     4.2e+9
     4.2e5
     42.e-7
     42.e+8
     42.e1
     42e-3
     42e+2
     42e4

To aid in the readability of large numbers, underscores may be inserted
anywhere within or at the end of a ``real`` literal as a separator. This
includes in the integer digits, in the mantissa, and throughout the
scientific notation. For example:

::

     ._____42__
     4_._2_e_-_1_2_

An underscore may **NOT** appear at the beginning of a ``real`` literal
because then it would be recognised as an identifier. For example, the
following would *not* be ``real`` literals:

::

     _.__4_2____
     ____4_._2
     _1_._e_-2

.. _sssec:real_ops:

Operations
~~~~~~~~~~

Floating point operations and precedence are equivalent to :ref:`integer operation and precedence <sssec:integer_ops>`.

Operations on real numbers should adhere to the IEEE 754 spec with
regards to the representation of not-a-number(NaNs), infiity(infs), and
zeros. A signaling NaN should cause a runtime error. Floating point
errors and semantics can be guaranteed by using the `LLVM IR constrained
floating point
intrinsics <https://llvm.org/docs/LangRef.html#constrained-floating-point-intrinsics>`__.
The ``round.towardzero`` rounding mode should be chosen along with the
``fpexcept.strict`` exception behaviour.

The runtime error cannot be enforced, but, if floating point semantics
are not constrained, then ``real`` values printed after operations may
not be identical.

**Assertion:** No floating point operation will create a runtime error.
(:ref:`safe-reals <assert:safe-reals>`)

For more information on why this is necessary, look into the `default
LLVM IR floating point
environment <https://llvm.org/docs/LangRef.html#floatenv>`__.

