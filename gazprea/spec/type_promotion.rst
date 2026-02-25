.. _sec:typePromotion:

Type Promotion
==============

Type promotion is a sub-problem of casting and refers to casts that happen
implicitly. Any conversion that can be done implicitly via promotion can also
be done explicitly via a typecast expression.

.. _ssec:typePromotion_lattice:

Type Lattice
------------

The diagram below shows every implicit promotion *Gazprea* permits. An arrow
``A → B`` means a value of type ``A`` can be silently converted to type ``B``
without an explicit ``as<>`` cast. Paths not shown require an explicit cast or
are entirely forbidden.

.. graphviz::

   digraph TypeLattice {
       rankdir=BT;
       node [shape=box, fontname="Courier", style=filled, fillcolor=white];
       edge [fontname="Courier", fontsize=10];

       // Scalar types
       subgraph cluster_scalars {
           label="Scalar Types";
           style=dashed;
           boolean  [label="boolean"];
           character [label="character"];
           integer  [label="integer"];
           real     [label="real"];
       }

       // The one scalar promotion
       integer -> real [label="implicit"];

       // Scalar-to-array (parametric — shown as a representative edge)
       scalar_T [label="T  (any scalar)", shape=ellipse, style=dashed];
       array_T  [label="T[…]  (array of T)", shape=ellipse, style=dashed];
       scalar_T -> array_T [label="broadcast\n(any compatible T)", style=dashed];

       // String / character[*] — bidirectional
       string      [label="string"];
       char_star   [label="character[*]"];
       string    -> char_star [label="implicit", dir=both];

       // Anonymous tuple promotion (field-wise)
       tup_src [label="tuple(A, B, …)\n[anonymous]",  shape=ellipse, style=dashed];
       tup_dst [label="tuple(A′, B′, …)\n[anonymous, A→A′]", shape=ellipse, style=dashed];
       tup_src -> tup_dst [label="field-wise\npromotion", style=dashed];
   }

Solid edges represent concrete implicit promotions between named types. Dashed
nodes and edges represent parametric promotion rules that apply to any
conforming type.

There are no other implicit promotions. In particular:

- ``real`` does **not** promote to ``integer`` (truncation requires ``as<>``).
- ``boolean`` and ``character`` have no implicit promotions to any other type.
- Array types do not implicitly downcast to scalars.

.. _ssec:typePromotion_scalar:

Scalars
-------

The only automatic type promotion for scalars is ``integer`` to ``real``.
This promotion is one-way — a ``real`` cannot be automatically converted to
``integer``.

+----------+-----------+---------+-----------+---------+---------------+
|          |                    **To type**                            |
+----------+-----------+---------+-----------+---------+---------------+
|          |           | boolean | character | integer |     real      |
+          +-----------+---------+-----------+---------+---------------+
| **From** |  boolean  |   id    |    N/A    |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
| **type** | character |   N/A   |    id     |   N/A   |      N/A      |
+          +-----------+---------+-----------+---------+---------------+
|          |  integer  |   N/A   |    N/A    |   id    | as<real>(var) |
+          +-----------+---------+-----------+---------+---------------+
|          |   real    |   N/A   |    N/A    |   N/A   |      id       |
+----------+-----------+---------+-----------+---------+---------------+

.. _ssec:typePromotion_stoa:

Scalar to Array
---------------

Any scalar type can be promoted to an array whose element type is compatible
with the scalar (per the scalar lattice above). This occurs when a scalar is
used in an operation with an array — the scalar is broadcast to match the
array's shape.

::

     integer i = 1;
     integer[5] v = [1, 2, 3, 4, 5];
     integer[5] res = v + i;

     res -> std_output;   // [2 3 4 5 6]

Other examples::

  1 == [1, 1]   // true — scalar broadcast into equality check
  1..2 || 3     // [1, 3] — 3 promoted to integer[1] then concatenated

Note that an array can never be downcast to a scalar, even with an explicit
cast. Matrix multiplication (``**``) also imposes strict dimensionality
requirements: scalar-to-matrix promotion under ``**`` is only permitted when
the matrix operand is square (:math:`m \times m`).

.. _ssec:typePromotion_tuple:

Tuple to Tuple
--------------

An anonymous tuple may be implicitly promoted to another anonymous tuple type
if both tuples have the same number of fields and each source field can be
implicitly promoted to the corresponding destination field type (per the scalar
lattice above).

Named fields do **not** participate in implicit promotion. See
:ref:`sssec:tuple_casting` for the full rules, including the behaviour of
mixed (partially-named) tuples.

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;   // Legal: anonymous, integer -> real

Two-sided promotion can occur when comparing anonymous tuples whose element
types differ — each side is promoted to the common type before comparison:

::

     boolean b = (1.0, 2) == (2, 3.0);   // (real, real) == (real, real)

.. _ssec:typePromotion_string:

Character Array to/from String
-------------------------------

A ``string`` can be implicitly converted to a ``character[*]`` and vice-versa.
This bidirectional promotion reflects that ``string`` is structurally a
``character[*]`` wrapper (see :ref:`ssec:string`). The compiler preserves the
type distinction for output-formatting purposes.

::

     string str1 = "Hello";
     character[5] chars = str1;                        // string -> character[5]
     string str2 = chars || [' ', 'W', 'o', 'r', 'l', 'd']; // character[*] -> string
