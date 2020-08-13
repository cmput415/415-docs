Generator
=========

A generator creates a series of numbers by applying an expression to the
value of an index. A generator is similar to a *C* style ``for`` loop.
For this assignment, the index variable will always start at the lower
bound and continue until it is equal to the upper bound (*the last value
of the index will be the upper bound*). The index will always be
incremented by the integer value 1. In *C*, this would be:

::

     for(int i = <start>; i <= <end>; ++i)

Generator Format
----------------

A generator statement will always follow the same format:

::

     [<id> in <int_1>..<int_2> | <expr>];

-  ``id`` is the identifier of the generator’s index.

-  ``int_1`` is an integer representing the lower bound of the generator

-  ``int_2`` is an integer representing the upper bound of the generator

-  ``expr`` is an expression

| **Assertion:** ``int_1`` and ``int_2`` will never be expressions, only
  integer literals. (:ref:`simple-bounds <assert:simple-bounds>`)
| **Assertion:** ``int_1`` will be never be greater than ``int_2``.
  (:ref:`sane-bounds <assert:sane-bounds>`)
| **Assertion:** If an identifier is used in ``expr`` then it will match
  ``id``. (:ref:`matching-id <assert:matching-id>`)

For this assignment the value of the identifier variable ``<id>``:

#. is initialized to the value of ``int_1``.

#. is used to evaluate the expression.

#. is incremented by one.

#. stops when its value is greater than ``int_2``.

For each value assumed by ``id``, ``expr`` is used to generated the next
number in the series.

Examples of valid generators:

::

     [i in 1..10 | i * i];
     [i in 0..10 | 2 ^ i];

In this assignment white space is not important so the following is
valid:

::

     [i
     in
     1
     ..
     10
     |
     i*i];
     [i in 1..10|2^i];

**Assertion:** Whitespace is guaranteed to be a space, a tab, a carriage
return, or a new line. (:ref:`simple-whitespace <assert:simple-whitespace>`)

Because identifiers need white space to separate each other the
following is invalid:

::

     [iin1..10|i*i];
     [i in1..10|2^i];
