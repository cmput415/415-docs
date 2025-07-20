.. _ssec:struct:

Structs
-------

Like ``tuples``, a ``struct`` is a way of grouping multiple values with
different types into an aggregate data structure.
The main differences between tuples and structs are that the fields of a struct
are named, and the type signature of a struct is named as a user defined type.
Any type except ``tuple`` and :ref:`streams<sec:streams>` may be stored within
a struct.

.. _sssec:struct_decl:

Declaration
~~~~~~~~~~~

A struct is declared with the keyword ``struct`` followed by a _type name_,
followed by a parentheses-surrounded, comma-separated list of
_field declarations_.
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

.. _sssec:struct_acc:

Access
~~~~~~

The fields of a struct are accessed using dot notation, as in tuples.
Dot notation can only be applied to struct instances and *not* struct literals.
Dot notation can be specified as ``<id>.<field>``, where:
  - ``id`` is an instance identifier/name of a struct of type ``T``
  - ``.`` is a literal period (dot)
  - ``field`` is a field within struct ``T``

For example:
::

     struct s1 (integer i, real r, integer[10] iv) t1;
     t1.i
     t1.iv[2]
     t1.r

Struct access can both be used as LVALs and as RVALs, i.e. on either the left
or right hand side of an expression:

::

     y = x + t1.r;     // Allowed
     t1.iv[i] = type-expr; // Allowed


.. _sssec:tuple_lit:

Literals
~~~~~~~~

A ``sturct`` literal is constructed by grouping values together between
parentheses in a comma separated list. For example:

::

     struct S (integer i, character[5] c, integer[3] a3) my_s = (x, "hello", [1, 2, 3]);
     var S s = (x, "hello", [1, 2, 3]);
     const S s = (x, "hello", [1, 2, 3]);
     struct V (integer i, real r, integer[10] arr) v = (1, 2.1, [i in 1..10 | i]);

.. _sssec:tuple_ops:

Operations
~~~~~~~~~~

The following operations are defined on ``struct`` instances.
In all of the usage examples, ``struct-type`` means some struct yielding
expression of a particular type, while ``id`` is a field within the struct.


+------------+---------------+------------+----------------------------  --+-------------------+
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

     struct Complex (real r, real i) c = (r, 0.0);
     if (c == (0.0, i)) { }

Two structs are equal when all fields within each struct have the same value.
It is an error to compare two structs of different types.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A struct itself cannot be cast or promoted. However, the fields within a struct
can be individually cast/promoted, as described in
sections :ref:`sec:typeCasting` and :ref:`sec:typePromotion`.
