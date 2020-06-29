.. _sec:errors:

Errors
======

The only error you need to support are are *static* type errors. Error
messages should be printed to the standard error stream.

.. _ssec:error_ops:

In Operations
-------------

These are type errors that occur in an expression when you cannot :ref:`implicitly convert <sec:typePromotion>` the
type of one operand to the type of the other. Errors should be printed
with the following form:

::

     Type error: Cannot convert between <lhs type> and <rhs type> on line <line number>

.. _sssec:error_ops_stos:

Between Scalars
~~~~~~~~~~~~~~~

Scalars are the simplest case and compare their type against another.
For example:

::

     procedure main() returns integer {
       int i = 'a' + 1;
     }

Should raise the following error:

::

     Type error: Cannot convert between character and integer on line 2

.. _sssec:error_ops_stovm:

Scalar to Vector/Matrix
~~~~~~~~~~~~~~~~~~~~~~~

In a scalar to ``vector`` or ``matrix`` conversion, the scalar’s type 
must be :ref:`implicitly convertable <sec:typePromotion>` to the element type
of the ``vector`` or ``matrix``. Note that this comparison can be
performed even if the size of the ``vector`` or ``matrix`` is unknown.
When printing the type of the ``vector`` or ``matrix``, include the
``vector`` part of the type, including size if it is known or an ``*``
otherwise. For example:

::

     procedure main() returns integer {
       var in = std_input();
       integer a;
       integer b;
       a <- in;
       b <- in;
       integer[3] v = as<integer[3]>('a' + [i in a..b | i]);
     }

Should raise the following error:

::

     Type error: Cannot convert between character and integer[*] on line 7

.. _sssec:error_ops_vtov:

Vector to Vector
~~~~~~~~~~~~~~~~

In a ``vector`` to ``vector`` conversion, one of the element types must
be :ref:`implicitly convertable <sec:typePromotion>` to the other element
type and the sizes of the each ``vector`` must match. The element type 
will always be known at compile time but if one or both of the sizes is not
known, then **NO STATIC TYPE CHECKING WILL BE PERFORMED**. 
For example, with differences in sizes:

::

     procedure main() returns integer {
       integer[3] a = [1, 2, 3];
       integer[2] b = [1, 2];
       integer[2] v = as<integer[2]>(a + b);
     }

Should raise the following error:

::

     Type error: Cannot convert between integer[3] and integer[2] on line 4

For example, with unconvertable element types:

::

     procedure main() returns integer {
       character[3] a = ['a', 'b', 'c'];
       integer[3] b = [1, 2, 3];
       integer[3] v = a + b;
     }

Should raise the following error:

::

     Type error: Cannot convert between character[3] and integer[3] on line 4

While there is potentially a runtime error in this example, there is no
compile time error because the size of ``d`` is unknowable:

::

     procedure main() returns integer {
       var in = std_input();
       integer a;
       integer b;
       a <- in;
       b <- in;
       integer[3] c = [1, 2, 3];
       integer[*] d = [i in a..b | i];
       integer[2] v = as<integer[2]>(c + d);
     }

.. _sssec:error_ops_mtom:

Matrix to Matrix
~~~~~~~~~~~~~~~~

In a ``matrix`` to ``matrix`` conversion, one of the element types must
be :ref:`implicitly convertable <sec:typePromotion>` to the other
element type and the sizes of the each ``matrix`` must
match. The element type will always be known at compile time but if one
or both of the sizes is not known, then **NO STATIC TYPE CHECKING WILL
BE PERFORMED**. For example, with differences in sizes:

::

     procedure main() returns integer {
       integer[2, 2] a = [[1, 2], [3, 4]];
       integer[1, 2] b = [[1, 2]];
       integer[2, 2] m = as<integer[2, 2]>(a + b);
     }

Should raise the following error:

::

     Type error: Cannot convert between integer[2, 2] and integer[1, 2]  on line 4

For example, with unconvertable element types:

::

     procedure main() returns integer {
       character[2, 2] a = [['a', 'b'], ['c', 'd']];
       integer[2, 2] b = [[1, 2], [3, 4]];
       integer[2, 2] m = a + b;
     }

Should raise the following error:

::

     Type error: Cannot convert between character[2, 2] and integer[2, 2] on line 4

While there is potentially a runtime error in this example, there is no
compile time error because the size of ``d`` is unknowable:

::

     procedure main() returns integer {
       var in = std_input();
       integer a;
       integer b;
       a <- in;
       b <- in;
       integer[2, 2] c = [[1, 2], [3, 4]];
       integer[*, *] d = [i in a..b, j in a..b | i * j];
       integer[2, 2] m = as<integer[2, 2]>(c + d);
     }

