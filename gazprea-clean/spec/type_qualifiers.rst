.. _sec:typeQualifiers:

Type Qualifiers
===============

*Gazprea* has two type qualifiers: ``const`` and ``var``. These
qualifers can prefix a type to specify its mutability or entirely
replace the type to request that it be inferred. Mutability refers to a
values ability to be an `r-value or
l-value <https://en.wikipedia.org/wiki/Value_(computer_science)#lrvalue>`__.
The two qualifiers cannot be combined as they are mutually exclusive.

.. _ssec:typeQualifiers_const:

Const
-----

A ``const`` value is immutable and therefore cannot be an l-value but
can be an r-value. For example:

::

     const integer i;

Because a ``const`` value is not an l-value, it cannot be passed to a
``var`` argument in a ``procedure``.

Note that ``const`` is the default *Gazprea* behaviour and is essentially a
no-op unless it is entirely replacing the type.


.. _ssec:typeQualifiers_var:

Var
---

A ``var`` value is mutable and therefore can be an l-value or r-value.
For example:

::

     var integer i;

The compiler should raise an error if an attempt is made to modify a variable
that is not explicitly declared ``var``.

.. _ssec:typeQualifiers_infer:

Type Inference Using Qualifiers
-------------------------------

Type qualifiers may be used in place of a type, in which case the real
type must be inferred. A variable declared in this manner must be
**immediately initialised** to enable inference. For example:

::

     var i = 1; // integer
     const i = 1; // integer
     var r = 1.0; // real
     const c = 'a'; // character
     var t = (1, 2, 'a', [1, 2, 3]); // tuple(integer, integer, character, integer[3])
     const v = ['a', 'b', 'c', 'd']; // character[4]

See :ref:`sec:typeInference` for a larger description of type inference, this section only
provides the syntax for inference using ``const`` and ``var``.
