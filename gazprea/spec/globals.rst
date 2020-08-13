.. _sec:global:

Globals
=======

In *Gazprea* values can be assigned to a global identifier. All globals
must be declared ``const``. If a global identifier is not declared with
the ``const`` specifier, then an error should be raised. This
restriction is in place since mutable global variables would ruin
functional purity. If functions have access to mutable global state then
we can not guarantee their purity.

Globals must be initialized, but the initialization expressions must not
contain any function calls, or procedures. If a global is initialized
with an expression containing a function call, or a procedure call, then
an error should be raised. Initializations of globals may refer to
previously defined globals.
