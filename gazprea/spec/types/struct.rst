.. _ssec:struct:

Structs
-------

Like ``tuples``, a ``struct`` is a way of grouping multiple values with
different types into an :term:`aggregate <aggregate type>` data structure.
The main differences between tuples and structs are that the fields of a struct
are named, and the type signature of a struct is named as a user-defined type.
Any :ref:`storable type <ssec:storable_types>` may be stored within a
struct, including arrays of any rank (a matrix is the rank-2 case),
``vector``, ``string``, ``tuple``, and other ``struct`` types, nested to any
depth (subject to the
:ref:`acyclicity rule <ssec:storable_types>`). Only
:ref:`streams<sec:streams>` may not be stored within a struct. Also like
tuples, structs must contain *at least two fields*; a ``struct`` type with fewer
than two fields is :term:`ill-formed`, and the compiler must emit a ``TypeError``
(see :ref:`sec:errors`).

.. _sssec:struct_decl:

Declaration
~~~~~~~~~~~

A struct is declared with the keyword ``struct`` followed by a *type name*,
followed by a parentheses-surrounded, comma-separated list of
*field declarations*.
Field declarations look identical to parameter declarations in functions,
and consist of a ``<type id>`` pair:

::

     struct s1 (integer i, real r, integer[10] iv) t1;
     struct Another (character ch, real f, string str, s1 struct_field);
     var Another t2;

The examples show two structs declared with types ``s1`` and ``Another``.
Struct type ``s1`` has three fields: ``i`` of type ``integer``, ``r`` of type
``real``, and ``iv`` of type ``integer[10]``.
Struct type ``Another`` has four fields named ``ch``, ``f``, ``str``,
and ``struct_field``.
The instance variables ``t1`` and ``t2`` have types ``s1`` and ``Another``,
respectively.

A struct declaration may optionally be followed by an identifier, as in
the first example: ``struct s1 (...) t1;`` declares the type ``s1`` *and*
a variable ``t1`` of that type in one statement, exactly equivalent to
``struct s1 (...); s1 t1;``. The combined form takes an optional qualifier
(``var`` or ``const``), exactly like any other
:ref:`declaration <sec:declaration>`: the bare ``struct s1 (...) t1;`` and
the explicit ``const struct s1 (...) t1;`` both declare an immutable ``t1``
(``const`` is the default), while ``var struct s1 (...) t1;`` declares a
mutable one. The split form, as the ``t2`` example shows, is equivalent.
A mutable struct instance such as ``var struct s1 (...) t1;`` (or the split
``var s1 t1;``) is legal in exactly the same positions as a mutable ``var``
:ref:`tuple <ssec:tuple>`.


.. _sssec:struct_typealias:


Type Aliasing
~~~~~~~~~~~~~

A struct type can be given a :ref:`type alias <sec:typealias>`. Like any type
alias (see :ref:`sec:typealias`), and like a plain struct *definition*, the
``typealias struct`` form may appear at global scope or inside a function or
procedure body; a local one is :term:`scoped <scope>` to its block and shadows
any outer type or alias of the same name. The combined form below both defines
the struct type ``S`` and introduces ``Pair`` as an alias for it: the struct's
own name ``S`` remains usable, for example as a literal constructor. Once
declared, the alias may be used in place of the struct's type name in type
positions. It may not, however, be used as a literal constructor.

::

    typealias struct S(integer x, integer y) Pair;

    function add(Pair p1, Pair p2) returns Pair {
        Pair p3 = S(x: p1.x + p2.x, y: p1.y + p2.y); // Pair cannot be used in place of S
        return p3;
    }


.. _sssec:struct_acc:

Access
~~~~~~

Struct fields are accessed with dot notation, ``instance.field``, where
``field`` is a field of the instance's struct type. For example:

::

     struct s1 (integer i, real r, integer[10] iv);
     var s1 t1;
     t1.i
     t1.iv[2]
     t1.r

Struct fields can be used as both :term:`lvalues <lvalue>` and
:term:`rvalues <rvalue>`, i.e. on either the left or right hand side of an
expression:

::

     y = x + t1.r;     // Allowed
     t1.iv[i] = type-expr; // Allowed


.. _sssec:struct_lit:

Literals
~~~~~~~~

A ``struct`` literal is constructed by listing comma separated ``field: value``
pairs for each field in the struct, surrounded by parentheses and prefaced by
the struct type name:

::

     struct S (integer i, character[5] c, integer[3] a3);
     const S cs = S(i: x, c: "hello", a3: [1, 2, 3]);
     var S vs = S(c: ' ', i: 0, a3: 0);
     struct V (integer i, real r, integer[10] arr) v = V(i: 1, r: 2.1, arr: [i in 1..11 | i]);

The fields may be listed in any order, but all fields must be present. The type
of each value must match, or be implicitly castable to (see
:ref:`sec:implicitCasts`), the type of the corresponding field definition in
the struct. A scalar value given for an array-typed field is implicitly cast to
fill the array, following the same scalar-to-array broadcast rule used for
array operations (see :ref:`sssec:array_ops`). Finally, note that the field
values may need to be evaluated at :term:`run time`.

.. _sssec:struct_ops:

Operations
~~~~~~~~~~

The following operations are defined on ``struct`` instances.
In all of the usage examples, ``struct-type`` means some struct yielding
expression of a particular type, while ``id`` is a field within the struct.

+------------+---------------+------------+--------------------------------+
| **Class**  | **Operation** | **Symbol** | **Usage**                      |
+------------+---------------+------------+--------------------------------+
| Access     | dot           | ``.``      | ``struct-type.id``             |
+------------+---------------+------------+--------------------------------+
| Comparison | equals        | ``==``     | ``struct-type == struct-type`` |
+            +---------------+------------+--------------------------------+
|            | not equals    | ``!=``     | ``struct-type != struct-type`` |
+------------+---------------+------------+--------------------------------+

Note that in the above table ``struct-type`` may only refer to a variable
instance for *Access*; accessing a field via dot notation on a non-variable
(for example, the result of an expression or a struct literal) must emit a
``TypeError`` (see :ref:`sec:errors`). For *Comparison*, **both** operands must
be structs of the same struct type ``T`` (one of them may be a struct literal,
since a struct literal already carries a struct type). A ``struct`` can only be
compared against another ``struct`` of the same type; there is no implicit cast
from a ``tuple`` to a ``struct``, so to compare a ``struct`` against a
``tuple`` the tuple's value must first be used to construct a ``struct`` of
type ``T``. Comparing two structs of different types is a ``TypeError`` (see
:ref:`sec:errors`). This rule still allows a struct instance to be compared to
a struct literal of the same type:

::

     struct Complex (real r, real i) c = Complex(r: r, i: 0.0);
     if (c == Complex(r: 0.0, i: i)) { }

Two structs are equal when all fields within each struct have the same value.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

.. _sssec:struct_casting:

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A struct itself cannot be cast or implicitly cast. However, the fields within a
struct can be individually cast or implicitly cast, as described in
sections :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`.

.. _sssec:struct_namespacing:

Struct Namespacing and Type Identity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Struct type identifiers live in the :ref:`type namespace <sec:namespaces>`,
which is :term:`lexically scoped <scope>`: a struct defined at global scope is
visible program-wide, while a struct defined inside a function or procedure
belongs only to that block and is **not** propagated outward. A struct
definition whose name matches one in an enclosing scope *shadows* it for the
rest of the block, just as a local variable shadows an outer one.

Structs are **nominal**: a struct's type identity is the *declaration* that
introduced it, not its field layout. Each ``struct`` (or ``typealias struct``)
declaration mints a fresh, distinct type, so two struct definitions have
different types even when their fields are identical -- including a local
definition that shadows a global one under the same name. A ``typealias``, by
contrast, introduces **no** new type: an alias is a transparent synonym that
carries the identity of whatever type it names (see :ref:`sec:typealias`), so an
alias of a struct *is* that struct's nominal type.

A variable's struct type is fixed at its declaration to whichever definition is
then in scope; a later redefinition of the name does not change it. Since
comparing two different struct types is a ``TypeError`` (see
:ref:`sssec:struct_ops`), this fixes exactly which comparisons are legal:

::

    typealias struct S(integer a, integer b) Pair; // global S; Pair == global S

    function f() returns integer {
        S    s1 = S(a: 2, b: 3);   // s1 : global S
        Pair p1 = S(a: 2, b: 3);   // p1 : Pair, i.e. global S

        // A new, distinct type despite identical fields; Pair now aliases it:
        typealias struct S(integer a, integer b) Pair; // local S

        S    s2 = S(a: 2, b: 3);   // s2 : local S
        Pair p2 = S(a: 2, b: 3);   // p2 : local S

        s1 == p1 -> std_output;    // T: both global S, equal field values
        s2 == p2 -> std_output;    // T: both local S
        s1 == s2 -> std_output;    // TypeError: global S vs local S
        p1 == p2 -> std_output;    // TypeError: global S vs local S
        s1 == p2 -> std_output;    // TypeError: global S vs local S
        s2 == p1 -> std_output;    // TypeError: local S vs global S
        return 1;
    }

A struct's field identifiers are not a namespace of their own: each struct
introduces its own :term:`declaration scope <scope>` for its fields, so a field
name may coincide with a type, a variable/function/procedure, or a field of
another struct, while the fields *within* one struct must be distinct. See
:ref:`sec:namespaces` for the full rules, including the ``SymbolError`` raised
when a struct declares two fields with the same name.
