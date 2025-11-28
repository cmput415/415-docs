.. _ssec:struct:

Structs
-------

Like ``tuples``, a ``struct`` is a way of grouping multiple values with
different types into an aggregate data structure.
The main differences between tuples and structs are that the fields of a struct
are named, and the type signature of a struct is named as a user defined type.
Any type except ``tuple``, another ``struct`` and :ref:`streams<sec:streams>`
may be stored within a struct. Also like tuples, structs must contain *at least two fields*.

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
     struct Another (character char, real float, string[256] str, s1 struct_field);
     var Another t2;

The examples show two structs declared with types ``s1`` and ``another``.
Struct type ``s`` has three fields: ``i`` of type ``integer``, ``r`` of type
``real``, and ``iv`` of type ``integer[10]``.
Struct type ``another`` has four fields named ``char``, ``float``, ``str``,
and ``struct_field``.
The instance variables are ``t1`` and ``t2`` have types ``s1`` and ``another``,
respectively.


.. _sssec:struct_typealias:


Type Aliasing
~~~~~~~~~~~~~

A struct can be typealiased and used in any context a regular struct declaration may occur. Notably, the alias can only be used in a type positions, not literal constructors. 

::
    
    typealias struct S(integer x, integer y) Pair;
    
    function add(Pair p1, Pair p2) returns Pair {
        Pair p3 = S(p1.x + p2.x, p1.y + p2.y); // Pair can not be used in place of S
        return p3;
    }
 

.. _sssec:struct_acc:

Access
~~~~~~

  * ``field`` is a field within struct ``T``

For example:
::

     struct s1 (integer i, real r, integer[10] iv) t1;
     t1.i
     t1.iv[2]
     t1.r

Struct fields can be used as both LVALs and RVALs, i.e. on either the left
or right hand side of an expression:

::

     y = x + t1.r;     // Allowed
     t1.iv[i] = type-expr; // Allowed


.. _sssec:struct_lit:

Literals
~~~~~~~~

A ``struct`` literal is constructed by listing comma separated values for each
field in the struct, in the order defined in the struct's definition.
The value list is surrounded by parenthesis and prefaced by the struct type:

::

     struct S (integer i, character[5] c, integer[3] a3);
     const S cs = S(x, "hello", [1, 2, 3]);
     var S vs = S(0, ' ', 0);
     struct V (integer i, real r, integer[10] arr) v = V(1, 2.1, [i in 1..10 | i]);

The type of each value in the list must match the type of the corresponding
field definition in the struct. To save having to explicitly specify a value
for each index in an array, *Gazprea* allows a single scalar to be propagated
across all elements in the array. Finally, note that the field values may need
to be evaluated at run-time.

.. _sssec:struct_ops:

Operations
~~~~~~~~~~

The following operations are defined on ``struct`` instances.
In all of the usage examples, ``struct-type`` means some struct yielding
expression of a particular type, while ``id`` is a field within the struct.

+------------+---------------+------------+--------------------------------+-------------------+
| **Class**  | **Operation** | **Symbol** | **Usage**                      | **Associativity** |
+------------+---------------+------------+--------------------------------+-------------------+
| Access     | dot           | ``.``      | ``struct-type.id``             | left              |
+------------+---------------+------------+--------------------------------+-------------------+
| Comparison | equals        | ``==``     | ``struct-type == struct-type`` | left              |
+            +---------------+------------+--------------------------------+-------------------+
|            | not equals    | ``!=``     | ``struct-type != struct-type`` | left              |
+------------+---------------+------------+--------------------------------+-------------------+

Note that in the above table ``struct-type`` may only refer to a variable
instance for *Access*, while for *Comparison* at least one of the operands must
resolve to a struct type ``T``.
This allows struct instances to be compared to struct literals:

::

     struct Complex (real r, real i) c = Complex(r, 0.0);
     if (c == Complex(0.0, i)) { }

Two structs are equal when all fields within each struct have the same value.
It is an error to compare two structs of different types.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A struct itself cannot be cast or promoted. However, the fields within a struct
can be individually cast/promoted, as described in
sections :ref:`sec:typeCasting` and :ref:`sec:typePromotion`.

.. _ssec:function_namespacing:

Struct Namespacing
--------------------

In *Gazprea*, struct declarations can occur in *any* scope.
This means that two struct types with the same name *can* coexist in the same
gazprea program so long as they are not in the same scope

Additionally, ``structs`` share the following namespaces:

-  The ``procedure`` namespace: You cannot have a procedure and struct with
   the same name in the same gazprea program.

-  The ``function`` namespace: You cannot have a function and struct with
   the same name in the same gazprea program.
