.. _ssec:tuple:

Tuple
-----

A ``tuple`` is a way of grouping multiple values with potentially
different types into one type. All types may be stored within tuples
except :ref:`streams <sec:streams>` and other tuples.

.. _sssec:tuple_decl:

Declaration
~~~~~~~~~~~

A ``tuple`` value is declared with the keyword ``tuple`` followed by a
parentheses-surrounded, comma-separated list of types. The list must
contain *at least two types*. Tuples are *mutable*. For example:

::

     tuple(integer, real, integer[10]) t1;
     tuple(character, real, string[256], real) t2;

The fields of a ``tuple`` may also be named. For example:

::

     tuple(integer, real r, integer[10]) t3;
     tuple(character mode, real, string[256] id, real) t4;

Here, ``t3`` has a named ``real`` field named ``r`` and ``t4`` has a
named ``character`` field named ``mode`` and another named ``string``
field named ``id``.

The number of fields in a ``tuple`` must be known at compile time. The only
exception is when a :ref:`variable is declared without a type using var or const <ssec:typeQualifiers_infer>`.
In this case, the variable must be initialised immediately with a literal whose type is known at compile time.

.. _sssec:tuple_acc:

Access
~~~~~~

The elements in a ``tuple`` are accessed using dot notation. Dot
notation can only be applied to ``tuple`` variables and *not* ``tuple``
literals. Therefore, dot notation is an identifier followed by a period
and then either a literal ``integer`` or a field name. Spaces are not
allowed inbetween elements in dot notation. Field indices
*start at one*, not zero. For example:

::

     t1.1
     t2.4
     t3.r
     t4.mode

Tuple access can both be used to retrieve the element value for an expression
as well as to assign a new value to the element.

::

     y = x + t1.1;     // Allowed
     t1.1 = type-expr; // Allowed


.. _sssec:tuple_lit:

Literals
~~~~~~~~

A ``tuple`` literal is constructed by grouping values together between
parentheses in a comma separated list. For example:

::

     tuple(integer, string[5], integer[3])  my_tuple = (x, "hello", [1, 2, 3]);
     var my_tuple = (x, "hello", [1, 2, 3]);
     const my_tuple = (x, "hello", [1, 2, 3]);
     tuple(integer, real r, integer[10]) tuple_var = (1, 2.1, [i in 1..10 | i]);

.. _sssec:tuple_ops:

Operations
~~~~~~~~~~

The following operations are defined on ``tuple`` values. In all of the
usage examples ``tuple-expr`` means some ``tuple`` yielding expression,
while ``int_lit`` is an ``integer`` literal as defined in :ref:`Integer Literals <sssec:integer_lit>` and ``id`` is
an identifier as defined in :ref:`sec:identifiers`.

+------------+---------------+------------+------------------------------+-------------------+
| **Class**  | **Operation** | **Symbol** | **Usage**                    | **Associativity** |
+------------+---------------+------------+------------------------------+-------------------+
| Access     | dot           | ``.``      | ``tuple-expr.int_lit``       | left              |
+            +               +            +                              +                   +
|            |               |            | ``tuple-expr.id``            |                   |
+------------+---------------+------------+------------------------------+-------------------+
| Comparison | equals        | ``==``     | ``tuple-expr == tuple-expr`` | left              |
+            +---------------+------------+------------------------------+-------------------+
|            | not equals    | ``!=``     | ``tuple-expr != tuple-expr`` | left              |
+------------+---------------+------------+------------------------------+-------------------+

Note that in the above table ``tuple-expr`` may refer to only a variable
for access. Accessing a literal could be replaced immediately with the
scalar inside the ``tuple`` literal. However ``tuple-expr`` may refer to
a literal in comparison operations to enable shorthand like this:

::

     if ((a, b) == (c, d)) { }

Comparisons are performed pairwise, therefore only ``tuple`` values of
the same type can be compared. This table describes how the comparisons
are completed, where t1 and t2 are ``tuple`` yielding expressions
including literals:

============= =========================================
**Operation** **Meaning**
============= =========================================
``t1 == t2``  ``t1.1 == t2.1 and ... and t1.n == t2.n``
``t1 != t2``  ``t1.1 != t2.1 or ... or t1.n != t2.n``
============= =========================================


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``tuple`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
