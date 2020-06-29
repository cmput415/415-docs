.. _sec:typedef:

Typedef
=======

Custom names for types can be defined using ``typedef``. Typedefs may
only appear at global scope, they may not appear within functions or
procedures. A typedef may use any valid identifier for the name of the
type. After the typedef has been defined any global declaration or
function defined may use the new name to refer to the old type. For
instance:

We can declare several vectors of 10 integers normally as such

::

       const integer a[10] = [i in 1..10 | 7];
       const integer b[10] = [i in 1..10 | 7];
       const integer c[10] = [i in 1..10 | 7];

or we can define a typedef for a vector of 10 integers for reusability.

::

       typedef integer[10] ten_ints;
       const ten_ints a = [i in 1..10 | 7];
       const ten_ints b = [i in 1..10 | 7];
       const ten_ints c = [i in 1..10 | 7];

Additionally, here is an example of using a matrix typedef:

::

       typedef integer[2,3] two_by_three_matrix;
       two_by_three_matrix m = [i in 1..2, j in 1..3 | i + j];

Typedefs of vectors and matrices with inferred sizes are allowed,
but declarations of variables using the typedef must be initialized. 
