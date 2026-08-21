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

An ``integer`` literal must be a representable ``i32`` value.

.. _sssec:integer_ops:

Operations
~~~~~~~~~~

The following operations are defined between ``integer`` values. In all
of the usage examples ``int-expr`` means some ``integer`` yielding
expression.

+------------+--------------------------+------------+--------------------------+
| **Class**  | **Operation**            | **Symbol** | **Usage**                |
+============+==========================+============+==========================+
| Grouping   | parentheses              | ``()``     | ``(int-expr)``           |
+------------+--------------------------+------------+--------------------------+
| Arithmetic | addition                 | ``+``      | ``int-expr + int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | subtraction              | ``-``      | ``int-expr - int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | multiplication           | ``*``      | ``int-expr * int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | division                 | ``/``      | ``int-expr / int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | remainder                | ``%``      | ``int-expr % int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | exponentiation           | ``^``      | ``int-expr ^ int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | unary negation           | ``-``      | ``- int-expr``           |
|            +--------------------------+------------+--------------------------+
|            | unary plus (no-op)       | ``+``      | ``+ int-expr``           |
+------------+--------------------------+------------+--------------------------+
| Comparison | less than                | ``<``      | ``int-expr < int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | greater than             | ``>``      | ``int-expr > int-expr``  |
|            +--------------------------+------------+--------------------------+
|            | less than or equal to    | ``<=``     | ``int-expr <= int-expr`` |
|            +--------------------------+------------+--------------------------+
|            | greater than or equal to | ``>=``     | ``int-expr >= int-expr`` |
|            +--------------------------+------------+--------------------------+
|            | equals                   | ``==``     | ``int-expr == int-expr`` |
|            +--------------------------+------------+--------------------------+
|            | not equals               | ``!=``     | ``int-expr != int-expr`` |
+------------+--------------------------+------------+--------------------------+

Unary negation produces the additive inverse of the ``integer``
expression. Unary plus always produces the same result as the
``integer`` expression it is applied to. Remainder mirrors the behaviour
of remainder in *C99*.

Exponentiation between integers gives an ``integer`` result. This is the same behavior as performing exponentiation on reals then truncating to an ``integer``.

Operator precedence and associativity are specified once, for all
types, in the :ref:`table of operator precedence
<ssec:expressions_toop>`.

Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``integer`` may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
