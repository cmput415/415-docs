.. _sec:namespaces:

Namespaces
==========

There are two namespaces in *Gazprea*:

- Type namespace: user-defined and builtin types (structs and typealiases).
- Variable/Function/procedure namespace: variables, functions, and
  procedures.

Items in separate namespaces may share an :term:`identifier`. Items within the
same namespace cannot share an identifier; the compiler must emit a
``SymbolError`` (see :ref:`sec:errors`).

Both namespaces are :term:`lexically scoped <scope>`. The no-sharing rule
applies within a single scope. A name introduced in an inner scope  **shadows**
any outer name of the same namespace for the extent of that scope and does not
leak back out. In particular, a type defined inside a function or procedure is
not added to the global type namespace.

A ``struct``'s field names can only collide with other field names in the same
struct. Each ``struct``
introduces its own :term:`declaration scope <scope>` for its fields, so a
field name lives in that struct's scope, not in either global namespace, and may
freely coincide with a type name, a variable/function/procedure name, or a field
name of another struct. On violation of unique field names in a struct
the compiler must emit a
``SymbolError`` (see :ref:`sec:errors`).

::

    // Does not conflict with the other statements
    struct x (integer a, integer b);

    // These three statements all conflict with each other
    // Any two of them in the same program produces a SymbolError
    integer x = 3;
    function x() returns integer;
    procedure x() returns integer;

The pro tip below relies on ``struct`` construction syntax, which is introduced
later in :ref:`ssec:struct`.

::

    // Pro tip: write code that looks like this, employers love it

    typealias integer a;
    typealias integer main; // Procedure and type do not conflict
    struct b (a b, a a, main main); // Struct field identifiers do not conflict with anything

    procedure main() returns integer {

        a a = 1; // type and variable do not conflict

        b b = b(b: a, a: 2, main: 3);

        if (true) { // New scope
            a a = b.b; // New `a` shadows the old `a`
        }
        return 0;
    }
