.. _ssec:real:

Real
----

A ``real`` is an IEEE 754 32-bit floating point value. A ``real`` can be
represented by a ``f32`` in *MLIR*.

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
multiplies the first literal by :math:`{10}^{x}`. For example,
:math:`4.2\mathrm{e}{-3}=4.2 \times10^{-3}`. For example:

::

     4.2e-1
     4.2e+9
     4.2E5
     42.e+37
     .42e-7
     42E6

.. _sssec:real_ops:

Operations
~~~~~~~~~~

Floating point operations and precedence are equivalent to :ref:`integer operation and precedence <sssec:integer_ops>`.

Operations on real numbers should adhere to the IEEE 754 spec with
regards to the representation of not-a-number(NaNs), infinity(infs), and
zeros.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``real`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
