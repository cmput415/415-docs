.. _sec:namespaces:

Namespaces
==========

There are two namespaces in *Gazprea*:

- Type namespace: user-defined types (structs and typealiases).
- Variable/Function/procedure namespace: functions and procedures.

Items in separate namespaces may share an identifier. Items within the same namespace cannot share an identifier, this is a ``SymbolError``.

::

    // Does not conflict with the other statements
    struct x (integer a, integer b);

    // These three statements all confict with each other
    // Any two of them in the same program produces a SymbolError
    integer x = 3;                   
    function x() returns integer;    
    procedure x() returns integer;            

::
    
    // Pro tip: write code that looks like this, employers love it

    typealias integer a;
    typealias integer main; // Procedure and type do not conflict
    struct b (a b, a a, main main); // Struct field identifiers do not conflict with anything

    procedure main() returns integer {
        
        a a = 1; // type and variable do not conflict

        b b = b(b: a, a: 2, main: 3);

        if (true) { // New scope
            a a = b.b // New `a` shadows the old `a`
        }
        return 0;
    }
