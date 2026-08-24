.. _sec:typeInference:

Type Inference
==============

*Gazprea* provides :term:`type inference`: in many cases the compiler can
figure out what a variable's type should be without an explicit type being
provided. For instance, instead of writing:

::

       integer x = 2;
       const integer y = x * 2;

*Gazprea* allows you to just write:

::

       var x = 2;
       const y = x * 2;

This is allowed because the compiler knows that the :term:`initializer`,
2, has the type integer. Because of this the compiler can automatically
give x an integer type. A *Gazprea* programmer can use ``var`` or
``const`` for any declaration with an initial value expression, as long
as the compiler can infer the type for the expression.

Note that although the qualifier may be elided (default is ``const``; see
:ref:`sec:typeQualifiers`) and the type may be elided (inferred from the
RHS), a declaration that elides both is :term:`ill-formed`:

::

       x = 2; // assignment or declaration?

Interpreted as a declaration, the full form would be ``const integer x = 2;``.
However, with both the modifier and type assumed, the compiler cannot
differentiate this declaration from an assignment statement. To prevent this
ambiguity, *Gazprea* requires at least one of the qualifier or the type to be
present:

::

       const integer x = 2; // full form - legal
       integer x = 2; // defaults to const - legal
       var x = 2; // infers integer - legal
       x = 2; // assignment to undeclared x - illegal
       var x; // can't infer type - illegal (TypeError)
       integer x; // const integer initialized to 0 - legal

Since neither the qualifier nor the type is present, ``x = 2;`` cannot be
parsed as a declaration and is instead an assignment; because ``x`` has not
been previously declared, the compiler must emit a ``SymbolError`` (see
:ref:`sec:errors`).

The declaration ``var x;`` is :term:`ill-formed` for a different reason: the
qualifier is present, so it *is* parsed as a declaration, but with the type
elided the compiler must infer it from an initializer -- and none is given.
Because the type cannot be resolved, the compiler must emit a ``TypeError``
(see :ref:`sec:errors`).
