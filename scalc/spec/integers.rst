Integers
--------

In this assignment, integers are the *only* numerical type (there is no
floating point type). As well, they are the only type that you can
store.

In this assignment integer literals are defined as being a string that
contains only the numerals 0-9 with no spaces.

| **Assertion:** All integer literals will be :math:`\geq 0`.
  (:ref:`nonnegative-literals <assert:nonnegative-literals>`)
| Examples of valid integers:

::

     1
     123
     5234
     01
     10

Examples of invalid integers:

::

     1.0
     one
     1_1
     1o

As well, integers *are* usable in conditions and must be *downcast* to
booleans. This means in a condtional, an integer that *is not* zero will
be considered true and an integer that *is* zero will be considered
false. For example:

::

     if (999)
       print(999);
     fi;
     if (0)
       print(0);
     fi;

produces the following output:

::

     999

