.. _sec:typedef:

Typedef
=======

Custom names for types can be defined using ``typedef``. Typedefs may only
appear at global scope, they may not appear within functions or procedures. A
typedef may use any valid identifier for the name of the type. After the typedef
has been defined any global declaration or function defined may use the new name
to refer to the old type. For instance:

::

  typedef integer int;
  const int a = 0;

Additionally, these new type names can conflict with symbol names. The
following is therefore legal:

::

  typedef character main;
  typedef integer i;

  const main A = 'A';

  procedure main() returns i {
    i i = 0;
    return i;
  }

In addition to base types, ``typedef`` can be used with vectors, matrices,
strings and tuples. Using ``typedef`` on tuples, or on vectors and matrices
with sizes helps reusability and consistency:

::

  typedef tuple(string[64], integer, real) student_id_grade;
  student_id_grade chucky_cheese = ("C. Cheese", 123456, 77.0);

  typedef integer[2,3] two_by_three_matrix;
  two_by_three_matrix m = [i in 1..2, j in 1..3 | i + j];

Typedefs of vectors and matrices with inferred sizes are allowed, but
declarations of variables using the typedef must be initialized appropriately.

Because ``typedef`` is an aliased name for a type, you can use
``typedef`` on typedef'ed types:

::

  typedef integer int;
  typedef int also_int;

Duplicate ``typedef`` should raise a `SymbolError`

::

  typedef integer ty;
  typedef character ty;

