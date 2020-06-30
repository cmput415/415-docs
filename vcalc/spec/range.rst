Range
-----

In *VCalc* the operator ``..`` is used to generate a vector holding a
range of integers. This operator must have an expression resulting in an
integer on both sides of it. These integers mark the *inclusive* upper
and lower bounds of the range.

For example:

::

     print(1..10);
     print((10-8)..(9+2));

prints the following:

::

     [1 2 3 4 5 6 7 8 9 10]
     [2 3 4 5 6 7 8 9 10 11]

The number of integers in a range may not be known at compile time when
the integer expressions use variables. In another example, assuming at
runtime that ``i`` is computed as -4:

::

     print(i..5);

prints the following:

::

     [-4 -3 -2 -1 0 1 2 3 4 5]

Therefore, it is *valid* to have bounds that will produce an empty
vector because the difference between them is negative. For example:

::

     int i = 3;
     int j = 0;
     print(i..j);

prints the following:

::

     []

