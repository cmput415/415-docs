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
       integer vector v[3] = as<integer vector[3]>('a' + [i in a..b | i]);
     }

Should raise the following error:

::

     Type error: Cannot convert between character and integer vector[*] on line 7

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
       integer vector a[3] = [1, 2, 3];
       integer vector b[2] = [1, 2];
       integer vector v[2] = as<integer vector[2]>(a + b);
     }

Should raise the following error:

::

     Type error: Cannot convert between integer vector[3] and integer vector[2] on line 4

For example, with unconvertable element types:

::

     procedure main() returns integer {
       character vector a[3] = ['a', 'b', 'c'];
       integer vector b[3] = [1, 2, 3];
       integer vector v[3] = a + b;
     }

Should raise the following error:

::

     Type error: Cannot convert between character vector[3] and integer vector[3] on line 4

While there is potentially a runtime error in this example, there is no
compile time error because the size of ``d`` is unknowable:

::

     procedure main() returns integer {
       var in = std_input();
       integer a;
       integer b;
       a <- in;
       b <- in;
       integer vector c[3] = [1, 2, 3];
       integer vector d[*] = [i in a..b | i];
       integer vector v[2] = as<integer vector[2]>(c + d);
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
       integer matrix a[2, 2] = [[1, 2], [3, 4]];
       integer matrix b[1, 2] = [[1, 2]];
       integer matrix m[2, 2] = as<integer matrix[2, 2]>(a + b);
     }

Should raise the following error:

::

     Type error: Cannot convert between integer matrix[2, 2] and integer matrix[1, 2]  on line 4

For example, with unconvertable element types:

::

     procedure main() returns integer {
       character matrix a[2, 2] = [['a', 'b'], ['c', 'd']];
       integer matrix b[2, 2] = [[1, 2], [3, 4]];
       integer matrix m[2, 2] = a + b;
     }

Should raise the following error:

::

     Type error: Cannot convert between character matrix[2, 2] and integer matrix[2, 2] on line 4

While there is potentially a runtime error in this example, there is no
compile time error because the size of ``d`` is unknowable:

::

     procedure main() returns integer {
       var in = std_input();
       integer a;
       integer b;
       a <- in;
       b <- in;
       integer matrix c[2, 2] = [['a', 'b'], ['c', 'd']];
       integer matrix d[*] = [i in a..b, j in a..b | i * j];
       integer matrix m[2, 2] = as<integer vector>[2](c + d);
     }

