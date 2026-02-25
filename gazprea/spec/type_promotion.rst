.. _sec:typePromotion:

Type Promotion
==============

Type promotion is a sub-problem of casting and refers to casts that happen
implicitly. Any conversion that can be done implicitly via promotion can also
be done explicitly via a typecast expression.

.. _ssec:typePromotion_lattice:

Type Lattice
------------

.. graphviz::

   digraph TypeLattice {
       rankdir=BT;
       compound=true;
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
       
       subgraph cluster_composite_types {
           label="Composite Types";
           style=dashed;
           //int_arr [label="integer[*]"];
           //real_arr [label="real[*]"];
           //bool_arr [label="boolean[*]"];
           char_arr     [label="char[*]"];
           string   [label="string"];
           generic_static_arr [label="U[*]  (static)", shape=ellipse, style=dashed]
           generic_dynamic_arr [label="U[*]  (dynamic)", shape=ellipse, style=dashed]
           generic_ragged_arr [label="U[..., *] (ragged)\nmust be explicitly initialized\nonly usable as data", shape=ellipse, style=dashed]
           //generic_static_arr -> int_arr [dir=none]
           //generic_static_arr -> real_arr [dir=none]
           generic_dynamic_arr -> char_arr [dir=none]
           //generic_static_arr -> bool_arr [dir=none]

            // String / character[*] - bidirectional
            string    -> char_arr [label="implicit", dir=both];
            generic_dynamic_arr -> string [dir=none]
            
            // arrays can implicitly promote to dynamic arrays but not vv
            generic_static_arr -> generic_dynamic_arr [label="implicit"]
       }
       
        subgraph cluster_aggregate_types {
           label="Aggregate Types";
           style=dashed;
           
            // Anonymous tuple promotion (field-wise)
            tup_tagged [label="tuple(name: U_1, name: T_2, ...)\ntagged"];
            tup_untagged [label="tuple(U_1, U_2, ...)\nuntagged"];
            tup_ptagged [label="tuple(name: U_1, U_2, ...)\npartially tagged"];
            tup_untagged -> tup_ptagged [label="implicit element-wise\ntype promotion"]
            tup_ptagged -> tup_tagged [label="implicit promotion if:\n- field names match\n- field types match\n- field orders match"]
            generic_tup [label="tuple  (generic)", shape=ellipse, style=dashed];
            tup_tagged -> generic_tup
            tup_ptagged -> generic_tup
            tup_untagged -> generic_tup
        }

        // The one scalar promotion
        integer -> real [label="implicit"];

        // Scalar-to-array (parametric - shown as a representative edge)
         scalar_T [label="T  (any scalar)", shape=ellipse, style=dashed];
         boolean -> scalar_T [lhead=cluster_scalars]
         real -> scalar_T [lhead=cluster_scalars]
         integer -> scalar_T [lhead=cluster_scalars]
         character -> scalar_T [lhead=cluster_scalars]
         
         scalar_T -> generic_static_arr [
          label="broadcast\n(any compatible T)", 
          style=dashed,
          ltail=cluster_composite_types
        ];
        
        union_type [label="U  (union of all types)", shape=ellipse, style=dashed];
        scalar_T -> union_type
        generic_static_arr -> union_type
        generic_dynamic_arr -> union_type
        generic_ragged_arr -> union_type
        generic_tup -> union_type

    }

The diagram above shows every implicit promotion *Gazprea* permits. An arrow
``A -> B`` means a value of type ``A`` can be silently converted to type ``B``
without an explicit ``as<>`` cast. Paths not shown require an explicit cast or
are entirely forbidden.

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

  1 == [1, 1]   // true - scalar broadcast into equality check
  1..2 || 3     // [1, 3] - 3 promoted to integer[1] then concatenated

Note that an array can never be downcast to a scalar, even with an explicit
cast. 

.. _ssec:typePromotion_tuple:

Tuple to Tuple
--------------

An anonymous tuple may be implicitly promoted to another anonymous tuple type
if both tuples have the same number of fields and each source field can be
implicitly promoted to the corresponding destination field type (per the scalar
lattice above).

Equivalently named fields are necessary, but not sufficient for implicit 
promotion. If promoting a named tuple, to another named tuple names, and
types must both match. If promoting a partially tagged tuple to another
partially tagged tuple, names, fields
and orders must all match between the two tuples. See
:ref:`sssec:tuple_casting` for additional elaboration, including the behaviour of
mixed (partially-named) tuples.

::

     tuple(integer, integer) int_tup = (1, 2);
     tuple(real, real) real_tup = int_tup;   // Legal: anonymous, integer -> real

Two-sided promotion can occur when comparing anonymous tuples whose element
types differ. Each side is promoted to the common type before comparison:

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
