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

We can also typedef vectors and matrices with sizes for easy reusability:

::

  typedef integer[10] ten_ints;
  const ten_ints a = [i in 1..10 | 7];

  typedef integer[2,3] two_by_three_matrix;
  two_by_three_matrix m = [i in 1..2, j in 1..3 | i + j];

Typedefs of vectors and matrices with inferred sizes are allowed, but
declarations of variables using the typedef must be initialized appropriately.
