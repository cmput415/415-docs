.. _sec:identifiers:

Identifiers
===========

:term:`Identifiers <identifier>` in *Gazprea* must start with either an
underscore or a letter (upper or lower cased). Subsequent characters can
be an underscore, letter (upper or lower case), or number. An identifier
may not be any of *Gazprea*\ 's keywords. Here are some valid identifiers
in *Gazprea*:

::

   	hello
   	h3ll0
   	_h3LL0
   	_Hi
   	Hi
   	_3

The following are some examples of :term:`ill-formed` identifiers.
They begin with a number, contain invalid characters, or are a keyword:

::

   	3d
   	in
   	a-bad-variable-name
   	no@twitter
   	we.don't.like.punctuation

*Gazprea* imposes no restrictions on the length of identifiers.

