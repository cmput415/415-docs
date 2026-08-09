.. _sec:typealias:

Typealias
=========

Custom names for types can be defined using ``typealias``. Type aliases may only
appear at global scope, they may not appear within functions or procedures. A
type alias may use any valid identifier for the name of the type. After the type
alias has been defined any global declaration or function defined may use the
new name to refer to the old type. For instance:

::

  typealias integer int;
  const int a = 0;

Note that these new type names can *appear* to conflict with symbol names.
However, the compiler can use context to differentiate a type alias from a
symbol. The following is therefore legal:

::

  typealias character main;
  typealias integer i;

  const main A = 'A';

  procedure main() returns i {
    i i = 0; // <type> <id> = <type-expr>;
    return i;
  }

In addition to :term:`primitive types <primitive type>`, ``typealias`` can be used
with compound types (arrays, vectors, and strings) and
:term:`aggregate types <aggregate type>` (structs and tuples).
Using ``typealias`` on tuples, or on arrays with sizes helps reusability and
consistency:

::

  typealias tuple(character[64], integer, real) student_id_grade;
  student_id_grade chucky_cheese = ("C. Cheese", 123456, 77.0);

  typealias integer[2][3] two_by_three_matrix;
  two_by_three_matrix m = [i in 1..2, j in 1..3 | i + j];

Type aliases of arrays with inferred sizes are allowed, but declarations
of variables using the type alias must be initialized appropriately.

Because a ``typealias`` is an aliased name for a type, you can use
``typealias`` on type alias'ed types:

::

  typealias integer int;
  typealias int also_int;

Duplicate alias names must emit a ``SymbolError`` (see :ref:`sec:errors`).

::

  typealias integer ty;
  typealias character ty;

Some type aliases may be parameterized with an expression, such as the size of
an array. Such size expressions must be valid
:ref:`constant expressions <sec:constexpr>`. This permits not only constant
folding of scalar literals but also constant propagation through other
``constexpr`` values, such as global constants.

::

  typealias integer[1 + 3 - 2] vec_of_two;
  procedure main() returns integer {
    vec_of_two v = 1..3;
  }

The compiler must emit a ``SizeError`` on line 3 since the ``vec_of_two``
type has a size of 2 and an array of size 3 is being assigned.

Because the size may be any ``constexpr``, it can reference other constant
expressions rather than being limited to literals:

::

  const WIDTH = 4;
  typealias integer[WIDTH] row;   // legal: WIDTH is a constexpr

