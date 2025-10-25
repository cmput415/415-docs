.. _sec:identifiers:

Identifiers
===========

Identifiers in *Gazprea* must start with either an underscore or a
letter (upper or lower cased). Subsequent characters can be an
underscore, letter (upper or lower case), or number. An identifier may
not be any of *Gazprea*\ ’s keywords. Here are some valid identifiers in
*Gazprea*:

::

   	hello
   	h3ll0
   	_h3LL0
   	_Hi
   	Hi
   	_3

The following are some examples of invalid identifiers. They begin with
a number, contain invalid characters, or are a keyword:

::

   	3d
   	in
   	a-bad-variable-name
   	no@twitter
   	we.don't.like.punctuation

*Gazprea* imposes no restrictions on the length of identifiers.

.. _ssec:namespace:

Namespaces
==========

Identifiers are used by variables, user-defined types, functions and procedures.

For the most part, user-defined types are in their own namespace because their
usage does not collide with variables or functions.
The one exception is that struct literals can look like function calls:

::

   struct A (integer i, real j);
   A a = A(i, j);

Consequently, struct literals and functions share the same namespace.
In the above example, a definition of function ``A`` should generate a
``SymbolError``, but a definition of variable ``A`` would not.
Outside of types, variables and functions/procedures share the same namespace
in a scope and shadowing is possible between these types.

::

   function x() returns integer; // "x" refers to this function in the global scope

   procedure main() {
     integer x = 3; // "x" refers to this variable in the scope of main
   }
   ...
