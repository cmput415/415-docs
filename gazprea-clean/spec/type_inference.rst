.. _sec:typeInference:

Type Inference
==============

In many cases the compiler can figure out what a variable’s type, or a
function’s return type, should be without an explicit type being
provided. For instance, instead of writing:

::

       integer x = 2;
       const integer y = x * 2;

*Gazprea* allows you to just write:

::

       var x = 2;
       const y = x * 2;

This is allowed because the compiler knows that the initialization
expression, 2, has the type integer. Because of this the compiler can
automatically give x an integer type. A *Gazprea* programmer can use
``var`` or ``const`` for any declaration with an initial value
expression, as long as the compiler can guess the type for the
expression.

Note that although the qualifier may be elided (default is ``const``) and the
type may be elided (inferred from the RHS), it is not legal to imply both:

::

       x = 2; // assignment or declaration?

Interpreted as a declaration, the full form would be ``const integer x = 2;``.
However, with both the modifier and type assumed we can't differentiate this
declaration from an assignment statement. To prevent this ambiguity, we require
at least one of the qualifier or the type to be present:

::

       const integer x = 2; // full form - legal
       integer x = 2; // defaults to const - legal
       var x = 2; // infers integer - legal
       x = 2; // assignment to undeclared variable? - illegal
       var x; // can't infer type - illegal
       integer x; // const integer initialized to 0 - legal
