.. _sec:namespaces:

Namespaces
==========

There are three namespaces in *Gazprea*:

- **Type namespace**: user-defined types (structs and typealiases).
- **Variable namespace**: variables.
- **Function/procedure namespace**: functions and procedures.

Because each occupies a separate namespace, a type, a variable, and a function
may all share the same name without conflict. However, functions and procedures
share a namespace, so a function and a procedure may *not* share a name.

::

   struct x (integer a, integer b); // type namespace — no conflict
   integer x = 3;                   // variable namespace — no conflict
   function x() returns integer;    // function/procedure namespace — no conflict
   // procedure x() { }             // ERROR: conflicts with function x
