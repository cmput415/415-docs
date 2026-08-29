.. _sec:typealias:

Typealias
=========

Custom names for types can be defined using ``typealias``. A type alias does
not introduce a new type: the alias name and the original type are the same
type by strong equivalence, and the two names may be used interchangeably
anywhere a type is expected. A ``typealias`` may be declared at global scope or inside a function or
procedure body. A local alias is :term:`scoped <scope>` to the block that
contains it and **shadows** any outer alias or type of the same name for the
rest of that block, without affecting the outer name outside it (two aliases
sharing a name in the *same* scope remain a conflict; see below). A type alias
may use any valid identifier for the name of the type. After the type alias has
been defined, the new name may be used anywhere the original type could be used.
For instance:

.. gazprea-example::
   :name: typealias_basic

   typealias integer int;
   const int a = 0;

   procedure main() returns integer {
     a -> std_output;
     return 0;
   }

   --- output ---
   0

Note that these new type names can *appear* to conflict with symbol names.
However, the compiler can use context to differentiate a type alias from a
symbol. The following is therefore legal:

.. gazprea-example::
   :name: typealias_symbol_context

   typealias character main;
   typealias integer i;

   const main A = 'A';

   procedure main() returns i {
     i i = 0; // <type> <id> = <expr>;
     return i;
   }

In addition to :term:`primitive types <primitive type>`, ``typealias`` can be
used with any :term:`aggregate type <aggregate type>` (arrays, matrices,
vectors, tuples, and structs), as well as with ``string``, itself a typealias
for ``vector<character>``.
Using ``typealias`` on tuples, or on arrays with sizes helps reusability and
consistency:

.. gazprea-example::
   :name: typealias_aggregate

   typealias tuple(character[64], integer, real) student_id_grade;
   typealias integer[2][3] two_by_three_matrix;

   procedure main() returns integer {
     student_id_grade chucky_cheese = ("C. Cheese", 123456, 77.0);
     two_by_three_matrix m = [i in 1..2, j in 1..3 | i + j];
     m -> std_output;
     return 0;
   }

   --- output ---
   [[2 3 4] [3 4 5]]

Type aliases of arrays with inferred sizes (``[*]``) are allowed, but
declarations of variables using the type alias must be initialized
appropriately (see :ref:`sssec:array_sizing`).

Because a ``typealias`` is an aliased name for a type, a ``typealias`` may
also be defined in terms of another ``typealias``:

.. gazprea-example::
   :name: typealias_of_typealias

   typealias integer int;
   typealias int also_int;

   procedure main() returns integer {
     also_int x = 5;
     x -> std_output;
     return 0;
   }

   --- output ---
   5

The compiler must emit a ``SymbolError`` (see :ref:`sec:errors`) for two aliases
that share a name *in the same scope*. (A local alias that shares its name with
one in an enclosing scope is not a conflict -- it shadows it, as above.)

.. gazprea-example::
   :name: typealias_conflict
   :error: SymbolError

   typealias integer ty;
   typealias character ty;

   procedure main() returns integer { return 0; }

Some type aliases may be parameterized with an expression, such as the size of
an array. Such size expressions must be valid
:ref:`constant expressions <sec:constexpr>`. This permits not only constant
folding of scalar literals but also constant propagation through other
``constexpr`` values, such as global constants.

::

  typealias integer[1 + 3 - 2] vec_of_two;
  procedure main() returns integer {
    vec_of_two v = 1..3;
    return 0;
  }

The compiler must emit a ``SizeError`` (see :ref:`sec:errors`) on line 3
since the ``vec_of_two`` type has a size of 2 and an array of size 3 is
being assigned.

Because the size may be any ``constexpr``, it can reference other constant
expressions rather than being limited to literals:

.. gazprea-example::
   :name: typealias_constexpr_size

   const WIDTH = 4;
   typealias integer[WIDTH] row;   // legal: WIDTH is a constexpr

   procedure main() returns integer {
     row r = [1, 2, 3, 4];
     r -> std_output;
     return 0;
   }

   --- output ---
   [1 2 3 4]

