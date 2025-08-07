.. _sec:global:

Globals
=======

In *Gazprea* values can be assigned to a global identifier. All globals
must be immutable (``const``). If a global identifier is declared with
the ``var`` specifier, then an error should be raised. This restriction is in
place since mutable global variables would ruin functional purity.
If functions have access to mutable global state then we can not guarantee
their purity.

Globals must be initialized, but the initialization expressions may only contain
literals.
That means that functions and even previously defined globals may not appear
on the RHS of a global declaration.
The reason is because it is very difficult to evaluate variables and functions
at compile time. Global expression evaluation could be deferred to runtime,
but that has the disadvantage of changing errors from compile time to run time.
