.. _ssec:tuple:

Tuples
------

A ``tuple`` is an ordered collection of values that groups multiple, potentially
different, types into a single compound value.

The fields within a tuple can be anonymous or can be given explicit names. This
allows tuples to be used as simple, lightweight collections or as more descriptive,
self-documenting data structures.

.. _sssec:tuple_structural:

Structural Tuples
~~~~~~~~~~~~~~~~~

By default, all tuple literals create **structural types**. A tuple's type is
uniquely defined by the sequence of its field types and their corresponding names.
The order of fields is significant, so two tuples `(integer a, real b)` and
`(real a, integer b)` are not equivalent.

**Type Identity**

The names of the fields are a part of the type. Therefore, two tuples with
different field names are considered different types, even if their underlying
member types are the same.

::

    // These three variables all have different, incompatible tuple types.
    var tuple (integer, real) a = (1, 2.0);
    var tuple (integer x, real y) b = (x: 1, y: 2.0);
    var tuple (integer a, real b) c = (a: 1, b: 2.0);

**Literals**

A tuple literal is constructed by grouping values together between parentheses
in a comma-separated list. Field names are optional and are specified with a
colon (`:`) after the name.

::

    // A literal of type (integer, character, boolean)
    (1, 'a', true)

    // A literal of type (integer x, real y)
    (x: 10, y: 3.14)

    // A literal of type (integer status, boolean)
    (status: 200, false)

Duplicate field names within a single tuple literal are not allowed and will
result in a compile-time error.

**Access**

Fields in a tuple are accessed using dot notation (`.`). Gazprea supports dual
access for named fields:

1.  **By Index:** All fields can be accessed by their 1-based integer index.
2.  **By Name:** If a field is named, it can also be accessed by its name.

::

    var point = (x: 10, y: 20);

    // Access by index
    point.1 -> std_output; // Prints 10
    point.2 = 30;         // Modify the second field

    // Access by name
    point.x -> std_output; // Prints 10
    point.y = 40;         // Modify the field named 'y'

.. _sssec:tuple_nominal:

Nominal Tuple Types
~~~~~~~~~~~~~~~~~~~

For stricter type safety, a tuple structure can be used to define a new
**nominal type** using the ``type`` keyword. A nominal type is distinct from all
other types, including structural tuples that have the exact same definition.

**Definition and Construction**

A nominal type is defined at the global scope. Instances of the type are created
using a constructor-like syntax where the type's name is used like a function.

::

    // Define a new, unique 'Point' type
    type Point = (integer x, integer y);

    // Construct an instance of the Point type
    var my_point = Point(x: 100, y: 200);

    // This is a type error, because Point and the structural tuple are not compatible
    // var another: Point = (x: 1, y: 2); // ILLEGAL

**Access**

Access for nominal types works identically to structural tuples, allowing access
by index or by name.

::

    my_point.x = 150;
    my_point.2 -> std_output; // Prints 200

.. _sssec:tuple_ops:

Operations
~~~~~~~~~~

**Comparison**

The equality (`==`) and inequality (`!=`) operators are defined for tuples.
Two tuples are considered equal if and only if:
1. They have a compatible type. For structural tuples, this means their type
   signatures (field types, names, and order) are identical. For nominal
   types, both must be of the same nominal type.
2. All corresponding fields are pairwise equal.

::

    var p1 = (x: 1, y: 2);
    var p2 = (x: 1, y: 2);
    var p3 = (a: 1, b: 2);

    p1 == p2; // true
    p1 == p3; // false (incompatible types)

    type Point = (integer x, integer y);
    var n1 = Point(x: 1, y: 2);
    var n2 = Point(x: 1, y: 2);

    n1 == n2; // true
    n1 == p1; // false (incompatible types: nominal vs. structural)

.. _sssec:tuple_casting:

Type Casting and Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~

**No Implicit Promotion**

Gazprea does not support implicit promotion or conversion between different
tuple types. If two tuple types are not identical, they are incompatible.

::

    var unnamed: (integer, integer) = (1, 2);
    var named: (integer x, integer y);

    named = unnamed; // ILLEGAL: types are not identical.

**Explicit Casting with `as<>`**

The `as<>` operator must be used to explicitly convert between compatible tuple
types. This is the only mechanism to:
1. Convert between different structural tuple types.
2. Convert a nominal tuple to its underlying structural type (or vice-versa).

The cast is only valid if the fields of the source tuple can be pairwise cast
to the fields of the destination type.

::

    // 1. Cast a structural literal to a named structural type
    var named: (integer x, integer y) = as<(integer x, integer y)>((1, 2));

    // 2. Cast between compatible nominal and structural types
    type Point = (integer x, integer y);
    var my_point = Point(x: 10, y: 20);

    // Cast from nominal to structural to call a generic procedure
    var structural_point = as<(integer x, integer y)>(my_point);

    // 3. Cast from a structural literal to a nominal type
    var another_point = as<Point>((x: 1, y: 2));