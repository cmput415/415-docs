.. _sec:typeQualifiers:

Type Qualifiers
===============

*Gazprea* has two :term:`type qualifiers <type qualifier>`: ``const`` and
``var``. These qualifiers can prefix a type to specify its mutability or
entirely replace the type to request that it be inferred. Mutability
refers to a value's ability to be an :term:`lvalue`: every value can be an
:term:`rvalue`, but only a mutable one can also be an lvalue. (An array slice is
an lvalue only as the target on the left of an assignment, and only when its
backing array is mutable; in every other position a slice is an ordinary array
value. See :ref:`sssec:array_slices`.)
The two qualifiers cannot be combined as they are mutually exclusive.

.. _ssec:typeQualifiers_const:

Const
-----

A ``const`` value is immutable and therefore cannot be an lvalue but
can be an rvalue. For example:

::

     const integer i;

Because a ``const`` value is not an lvalue, it cannot be passed to a
``var`` parameter in a ``procedure``; the compiler must emit a
``TypeError`` (see :ref:`sec:errors`).

``const`` is the default in *Gazprea*: a declaration with no qualifier
declares a ``const`` variable. Both ``T x`` (qualifier elided) and
``const T x`` (qualifier written explicitly) are legal spellings of the
same declaration. Writing ``const`` is therefore redundant, except where
the qualifier entirely replaces the type (see
:ref:`ssec:typeQualifiers_infer`).

.. This section is the normative home of the const-by-default rule; other
   chapters reference it.


.. _ssec:typeQualifiers_var:

Var
---

A ``var`` value is mutable and therefore can be an lvalue or rvalue.
For example:

::

     var integer i;

The compiler must emit an ``AssignError`` (see :ref:`sec:errors`) if an
attempt is made to modify a variable that is not explicitly declared
``var``.

.. _ssec:typeQualifiers_infer:

Type Inference Using Qualifiers
-------------------------------

Type qualifiers may be used in place of a type, in which case the
compiler must infer the real type. A variable declared in this manner must be
**immediately initialized** to enable inference. For example:

::

     var i = 1; // integer
     const j = 1; // integer
     var r = 1.0; // real
     const c = 'a'; // character
     var t = (1, 2, 'a', [1, 2, 3]); // tuple(integer, integer, character, integer[3])
     const v = ['a', 'b', 'c', 'd']; // character[4]

See :ref:`sec:typeInference` for a larger description of type inference; this
section only provides the syntax for inference using ``const`` and ``var``.
