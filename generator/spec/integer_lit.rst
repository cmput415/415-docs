Integer Literals
================

In this assignment integer literals are defined as being a string that
contains only the number characters 0-9 with no spaces.

| **Assertion:** All integer literals will be :math:`\geq 0`.
  (:ref:`nonnegative-literals <assert:nonnegative-literals>`)
| **Assertion:** All integer literals will fit in 31 unsigned bits.
  (:ref:`literal-size <assert:literal-size>`)

Examples of valid integers literals:

::

     1
     123
     5234
     01
     10

Examples of invalid integers literals:

::

     -1
     1.0
     one
     1_1
     1o
     4294967296

