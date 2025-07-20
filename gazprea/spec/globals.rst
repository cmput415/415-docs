.. _sec:global:

Globals
=======

In *Gazprea* values can be assigned to a global identifier. All globals
must be immutable (``const``). If a global identifier is declared with
the ``var`` specifier, then an error should be raised. This restriction is in
place since mutable global variables would ruin functional purity.
If functions have access to mutable global state then we can not guarantee
their purity.

Globals must be initialized, but the initialization expressions must not contain
any function calls or procedures. If a global is initialized with an expression
containing a function or procedure call, then an error should be raised.
Initializations of globals may refer to previously defined globals.
