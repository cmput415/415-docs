.. _ssec:tuple:

Tuples
------

A ``tuple`` is an ordered collection of values that groups multiple, potentially
different, types into a single compound value.

The fields within a tuple can be anonymous or can be given explicit names. This
allows tuples to be used as simple, lightweight collections or as more descriptive,
self-documenting data structures.

.. _sssec:tuple_decl:

Declaration
~~~~~~~~~~~

A tuple type is declared using the ``tuple`` keyword followed by a
parenthesised, comma-separated list of field type specifiers. Each field may
optionally carry a name:

::

    // Anonymous fields — accessed by index only.
    tuple(integer, real) a;

    // Named fields — accessed by index or by name.
    tuple(integer x, real y) b;

The default qualifier applies: a declaration without ``var`` is ``const``.

**Type Identity**

Field names are part of the type. The rules are:

- A **named field** contributes both its name and its type to the type identity.
  Two named fields at the same position are compatible only if they share the
  same name.
- An **unnamed field** contributes only its type to the type identity. An
  unnamed field at position *i* in one tuple is compatible with an unnamed field
  at position *i* in another tuple based solely on type compatibility.
- A named field and an unnamed field at the same position are **never**
  compatible, even if the underlying types match.

Therefore, two tuples whose fields have the same underlying types but different
names (or a mix of named and unnamed) are considered different, incompatible types:

::

    // These three variables have different, incompatible types.
    tuple(integer, real) a = (1, 2.0);          // fully anonymous
    tuple(integer x, real y) b = (x: 1, y: 2.0); // fully named
    tuple(integer a, real b) c = (a: 1, b: 2.0); // different names from b

    // Mixed: field 1 is named x, field 2 is anonymous, field 3 is named z.
    tuple(integer x, real, character z) mixed = (x: 1, 2.0, z: 'a');

    // Incompatible with mixed: field 2 has a name (y) where mixed has none.
    tuple(integer x, real y, character z) named = (x: 1, y: 2.0, z: 'a');

    mixed == named; // ILLEGAL: field 2 is unnamed in mixed, named in named

.. _sssec:tuple_lit:

Literals
~~~~~~~~

A tuple literal is constructed by grouping values together between parentheses
in a comma-separated list.

**Fully named tuples** may use named field syntax, where each value is preceded
by its field name and a colon (``:``)  Named literals may appear in any order,
since the names provide unambiguous mapping to fields:

::

    // A literal of type tuple(integer x, real y) — names in order
    (x: 10, y: 3.14)

    // Same type, names out of order — legal because all fields are named
    (y: 3.14, x: 10)

**Anonymous or mixed tuples must be constructed positionally.** When any field
in a tuple type is unnamed, the entire literal must list values in declaration
order with no field name labels:

::

    // tuple(integer, character, boolean) — all anonymous, positional only
    (1, 'a', true)

    // tuple(integer x, real, character z) — mixed: positional only
    (1, 2.0, 'a')

.. note::

   **Rationale.** Allowing named labels in a mixed-tuple literal would make
   ordering ambiguous as soon as more than one field is unnamed. For example,
   given ``tuple(integer x, real, character z)``, the literal
   ``(z: 'a', 2.0, x: 1)`` looks as though it reorders fields, but the unnamed
   ``real`` field has no label to anchor it — it could plausibly bind to position
   1, 2, or 3. Requiring fully positional construction for any tuple that contains
   an unnamed field eliminates this ambiguity entirely and keeps the rule simple:
   if you need named literals, name all of your fields.

Duplicate field names within a single tuple literal are not allowed and will
result in a compile-time error.

.. _sssec:tuple_access:

Access
~~~~~~

Fields in a tuple are accessed using dot notation (``.``). *Gazprea* supports
dual access for named fields:

1. **By Index:** All fields can be accessed by their 1-based integer index.
2. **By Name:** If a field is named, it can also be accessed by its name.

::

    var point = (x: 10, y: 20);

    // Access by index
    point.1 -> std_output; // Prints 10
    point.2 = 30;          // Modify the second field

    // Access by name
    point.x -> std_output; // Prints 10
    point.y = 40;          // Modify the field named 'y'

.. _sssec:tuple_ops:

Operations
~~~~~~~~~~

**Comparison**

The equality (``==``) and inequality (``!=``) operators are defined for tuples.
Two tuples are considered equal if and only if:

1. They have a compatible type (see :ref:`sssec:tuple_casting`).
2. All corresponding fields are pairwise equal.

::

    tuple(integer x, integer y) p1 = (x: 1, y: 2);
    tuple(integer x, integer y) p2 = (x: 1, y: 2);
    tuple(integer a, integer b) p3 = (a: 1, b: 2);
    tuple(integer, integer)     p4 = (1, 2);

    p1 == p2; // true: same type, same values
    p1 == p3; // ILLEGAL: incompatible types — field names differ (x/y vs a/b)
    p1 == p4; // ILLEGAL: incompatible types — p1 has named fields, p4 has none

.. _sssec:tuple_casting:

Type Casting and Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Implicit Promotion (Anonymous Fields Only)**

Implicit promotion between tuple types is permitted only at positions where
**both** the source and destination fields are unnamed. At such positions, the
normal scalar promotion rules apply (e.g. ``integer`` promotes to ``real``).
Named fields are never implicitly promoted; if either the source or destination
field carries a name, an explicit ``as<>`` cast is required for that conversion.

::

    // Fully anonymous: field-wise promotion applies freely.
    tuple(integer, integer) int_tup = (1, 2);
    tuple(real, real) real_tup = int_tup;  // Legal: both fields anonymous, integer -> real

    // Mixed: the unnamed field (position 2) promotes; named fields must match exactly.
    tuple(integer x, integer, character z) src = (x: 1, 2, z: 'a');
    tuple(integer x, real,    character z) dst = src;  // Legal: position 2 is unnamed in both

    // Named fields do NOT implicitly promote.
    tuple(integer x, integer y) named = (x: 1, y: 2);
    tuple(real x, real y) named_real = named;  // ILLEGAL: named fields require as<>

    // Must use explicit cast:
    tuple(real x, real y) named_real = as<tuple(real x, real y)>(named);

**Explicit Casting with ``as<>``**

The ``as<>`` operator can be used to explicitly convert between compatible tuple
types. The cast is valid if the source and destination have the same number of
fields and each source field can be cast (per :ref:`sec:typeCasting`) to the
corresponding destination field type.

::

    // Cast an anonymous tuple to a named type
    tuple(integer x, integer y) named = as<tuple(integer x, integer y)>((1, 2));

    // Cast between named tuple types with compatible field types
    tuple(integer a, integer b) ab = (a: 3, b: 4);
    tuple(real x, real y) xy = as<tuple(real x, real y)>(ab);
