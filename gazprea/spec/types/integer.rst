.. _ssec:integer:

Integer
-------

An ``integer`` is a signed 32-bit value. An ``integer`` can be
represented by an ``i32`` in *LLVM IR*.

.. _sssec:integer_decl:

Declaration
~~~~~~~~~~~

A ``integer`` value is declared with the keyword ``integer``.

.. _sssec:integer_null:

Null
~~~~

``null`` is ``0`` for ``integer``.

.. _sssec:integer_ident:

Identity
~~~~~~~~

``identity`` is ``1`` for ``integer``.

.. _sssec:integer_lit:

Literals
~~~~~~~~

An ``integer`` literal is specified in base 10. For example:

::

     1234
     2
     0

To aid in the readability of large numbers, underscores may be inserted
anywhere within or at the end of an ``integer`` literal as a separator.
For example, the following literals would produce the same ``integer``
value:

::

     1__23_4
     1234
     1_2_3_4___

An underscore may **NOT** appear at the beginning of an ``integer``
literal because then it would be recognised as an identifier. For
example, the following would be identifiers and *not* ``integer``
literals:

::

     _2
     ____2_3
     _2__3_

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
+            +--------------------------+------------+--------------------------+-------------------+
|            | subtraction              | ``-``      | ``int-expr - int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | multiplication           | ``*``      | ``int-expr * int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | division                 | ``/``      | ``int-expr / int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | remainder                | ``%``      | ``int-expr % int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | exponentiation           | ``^``      | ``int-expr ^ int-expr``  | right             |
+            +--------------------------+------------+--------------------------+-------------------+
|            | unary negation           | ``-``      | ``- int-expr``           | right             |
+            +--------------------------+------------+--------------------------+-------------------+
|            | unary plus (no-op)       | ``+``      | ``+ int-expr``           | right             |
+------------+--------------------------+------------+--------------------------+-------------------+
| Comparison | less than                | ``<``      | ``int-expr < int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | greater than             | ``>``      | ``int-expr > int-expr``  | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | less than or equal to    | ``<=``     | ``int-expr <= int-expr`` | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | greater than or equal to | ``>=``     | ``int-expr >= int-expr`` | left              |
+            +--------------------------+------------+--------------------------+-------------------+
|            | equals                   | ``==``     | ``int-expr == int-expr`` | left              |
+            +--------------------------+------------+--------------------------+-------------------+
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
+                +                +
|                | ``unary -``    |
+----------------+----------------+
|                | ``^``          |
+----------------+----------------+
|                | ``*``          |
+                +                +
|                | ``/``          |
+                +                +
|                | ``%``          |
+----------------+----------------+
|                | ``+``          |
+                +                +
|                | ``-``          |
+----------------+----------------+
|                | ``<``          |
+                +                +
|                | ``>``          |
+                +                +
|                | ``<=``         |
+                +                +
|                | ``>=``         |
+----------------+----------------+
|                | ``==``         |
+                +                +
| LOWER          | ``!=``         |
+----------------+----------------+
