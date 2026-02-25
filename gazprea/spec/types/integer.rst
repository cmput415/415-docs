.. _ssec:integer:

Integer
-------

An ``integer`` is a signed 32-bit value. An ``integer`` can be
represented by an ``i32`` in *MLIR*.

.. _sssec:integer_decl:

Declaration
~~~~~~~~~~~

A ``integer`` value is declared with the keyword ``integer``.

.. _sssec:integer_lit:

Literals
~~~~~~~~

An ``integer`` literal is specified in base 10. For example:

::

     1234
     2
     0

.. _sssec:integer_ops:

Operations
~~~~~~~~~~

The following operations are defined between ``integer`` values. In all
of the usage examples ``int-expr`` means some ``integer`` yielding
expression.

+------------+--------------------------+------------+--------------------------+-------------------+
| **Class**  | **Operation**            | **Symbol** | **Usage**                | **Associativity** |
+============+==========================+============+==========================+===================+
| Grouping   | parentheses              | ``()``     | ``(int-expr)``           | N/A               |
+------------+--------------------------+------------+--------------------------+-------------------+
| Arithmetic | addition                 | ``+``      | ``int-expr + int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | subtraction              | ``-``      | ``int-expr - int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | multiplication           | ``*``      | ``int-expr * int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | division                 | ``/``      | ``int-expr / int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | remainder                | ``%``      | ``int-expr % int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | exponentiation           | ``^``      | ``int-expr ^ int-expr``  | right             |
|            +--------------------------+------------+--------------------------+-------------------+
|            | unary negation           | ``-``      | ``- int-expr``           | right             |
|            +--------------------------+------------+--------------------------+-------------------+
|            | unary plus (no-op)       | ``+``      | ``+ int-expr``           | right             |
+------------+--------------------------+------------+--------------------------+-------------------+
| Comparison | less than                | ``<``      | ``int-expr < int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | greater than             | ``>``      | ``int-expr > int-expr``  | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | less than or equal to    | ``<=``     | ``int-expr <= int-expr`` | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | greater than or equal to | ``>=``     | ``int-expr >= int-expr`` | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | equals                   | ``==``     | ``int-expr == int-expr`` | left              |
|            +--------------------------+------------+--------------------------+-------------------+
|            | not equals               | ``!=``     | ``int-expr != int-expr`` | left              |
+------------+--------------------------+------------+--------------------------+-------------------+

Unary negation produces the additive inverse of the ``integer``
expression. Unary plus always produces the same result as the
``integer`` expression it is applied to. Remainder mirrors the behaviour
of remainder in *C99*.

This table specifies ``integer`` operator precedence. Operators without
lines between them have the same level of precedence. Note that
parentheses are not included in this list because they are used to
override precedence and create new atoms in an expression.

+----------------+----------------+
| **Precedence** | **Operations** |
+================+================+
| HIGHER         | ``unary +``    |
|                |                |
|                | ``unary -``    |
+----------------+----------------+
|                | ``^``          |
+----------------+----------------+
|                | ``*``          |
|                |                |
|                | ``/``          |
|                |                |
|                | ``%``          |
+----------------+----------------+
|                | ``+``          |
|                |                |
|                | ``-``          |
+----------------+----------------+
|                | ``<``          |
|                |                |
|                | ``>``          |
|                |                |
|                | ``<=``         |
|                |                |
|                | ``>=``         |
+----------------+----------------+
|                | ``==``         |
|                |                |
| LOWER          | ``!=``         |
+----------------+----------------+


Overflow
~~~~~~~~

``integer`` arithmetic is checked at runtime. If the result of an operation
exceeds the range of a signed 32-bit integer (i.e. falls outside
−2,147,483,648 to 2,147,483,647), a runtime ``OverflowError`` is raised.
Overflow does **not** wrap silently.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``integer`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
