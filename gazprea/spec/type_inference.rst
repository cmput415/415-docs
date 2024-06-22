.. _sec:typeInference:

Type Inference
==============

In many cases the compiler can figure out what a variable’s type, or a
function’s return type should be without an explicit type being
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
