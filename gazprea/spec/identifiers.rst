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

Namespace
===========

Identifiers are used by variables, functions and procedures.

These share the same namespace in a scope and shadowing
is possible between these types.

::

   function x() returns 1; // "x" refers to this function in the global scope
   
   {
     integer x = 3; // "x" refers to this variable in the block scope
   }
