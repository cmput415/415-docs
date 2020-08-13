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

One case where ``var`` or ``const`` will lead to an error is if the
initial value is a polymorphic constant such as ``null``, or
``identity``. *Gazprea*\ ’s type inference is simple, and only relies
upon a single expression, so it can not discover the type of x in:

::

       var x = null;  /* Can't tell what type this is */
       const y = identity; /* Can't tell what type this is either */
       integer z = x;

Clearly the type that makes the most sense for x here would by
``integer``, but *Gazprea* only checks the initialization expression,
and does not see how the variable x is used across statements. As a
result an error should be raised in this situation.

*Gazprea* employs a very simple type inference algorithm on expressions.
It finds the type that makes sense across binary expressions in a bottom
up fashion. For instance:

::

       /* The type for 'x' can be infered to be an integer. This expression
          can be rewritten as (null + 1) + null. The type inference algorithm
          checks (null + 1), and decides that since 1 is an integer 'null'
          must also be an integer because '+' can only be applied to numbers
          of the same type. Similarly it then infers that since (null + 1) is
          an integer (null + 1) + null is an integer as well, thus 'x' must
          be an integer. */

       var x = null + 1 + null;

       /* The simple type inference algorithm can not handle this case, and a
          type ambiguity error should be raised. Since this expression is
          (null + null) + 1 the type inference algorithm will try to figure
          out the type for (null + null), but since it doesn't know what
          either of the null values types are it can't. */

       var y = null + null + 1;
