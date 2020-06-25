.. _ssec:interval:

Interval
--------

An ``interval`` is used to represent ranges of values. *Gazprea* only
has support for an ``integer`` ``interval``.

.. _sssec:inteval_decl:

Declaration
~~~~~~~~~~~

An ``interval`` is declared with the keyword ``interval``. Only the
``integer`` base type for intervals is supported by *Gazprea*. For
example:

::

     integer interval iv;

.. _sssec:interval_null:

Null
~~~~

``null`` is defined as ``null..null``. For the ``integer`` ``interval``
this is ``0..0``.

.. _sssec:interval_ident:

Identity
~~~~~~~~

``identity`` is defined as ``identity..identity``. For the ``integer``
``interval`` this is ``1..1``.

.. _sssec:interval_lit:

Literals
~~~~~~~~

An ``interval`` literal is a range expression, created using two
inclusive bounds and the range operator (``..``). For example, a range
from one to ten, including the endpoints:

::

     integer interval i = 1..10;

.. _sssec:interval_ops:

Operations
~~~~~~~~~~

Operations on intervals should follow the standard rules of `interval
arithmetic <http://en.wikipedia.org/wiki/Interval_arithmetic>`__. In
each case integer operations should be used, for instance interval
division should use integer division. For another explanation see `this
website <http://www.csgnetwork.com/directintervalcalc.html>`__ under the
heading of “How the operations work”.

In the following table ``ivl-expr`` means any expression that yields an
``interval`` value and ``int-expr`` means any ``integer`` yielding
expression.

========== ================== ========== ======================== =================
**Class**  **Operation**      **Symbol** **Usage**                **Associativity**
========== ================== ========== ======================== =================
Arithmetic addition           ``+``      ``ivl-expr + ivl-expr``  left
\          subtraction        ``-``      ``ivl-expr - ivl-expr``  left
\          multiplication     ``*``      ``ivl-expr * ivl-expr``  left
\          division           ``/``      ``ivl-expr / ivl-expr``  left
\          unary negation     ``-``      ``- ivl-expr``           right
\          unary plus (no-op) ``+``      ``+ ivl-expr``           right
Comparison equals             ``==``     ``ivl-expr == ivl-expr`` left
\          not equals         ``!=``     ``ivl-expr != ivl-expr`` left
Vector     vector creation    ``by``     ``ivl-expr by int-expr`` left
========== ================== ========== ======================== =================

Regarding the semantics of some of the operators:

-  Comparison checks the bounds of each ``interval``.

-  Range upper bounds must greater than or equal to the lower bound.

-  Both bounds must be ``integer`` valued.

The precedence and associativity follows that of for the operators
defined in the above table, with the addition of the ``by`` and ``..``
operators, in the following table. The ``.`` and ``[]`` operators are
included for clarification but for the full table see .

============== ==============
**Precedence** **Operations**
============== ==============
HIGHER         ``.``
\              ``[]``
\              ``..``
\              arithmetic ops
\              ``by``
LOWER          comparison ops
============== ==============

This means that ``by`` is the lowest priority and so last binding
operator, therefore each side of the expression will be evaluated before
evaluating the ``by`` operator. As well, ``..`` is the highest priority
and first binding operator, excluding the ``.`` and ``[]`` operators
which create atoms, and will bind to atoms before other operators. For
example:

::

     1 .. 10 by 3
     a[1] .. b.3 by 1 + 2

Should be parsed as:

::

     (((1) .. (10)) by (3))
     (((a[1]) .. (b.3)) by ((1) + (2)))

Some tricky cases, for example:

::

     1 + 1 .. 10
     - 1 .. 10

Should be parsed as:

::

     (1 + (1 .. 10))
     (- (1 .. 10))

The first of which is *illegal* while the second is legal but
potentially *unexpected*. For the first, there is no addition operator
defined between an ``integer`` and an ``interval``. Second, the unary
``-`` will be applied to the entire range not just the first operand.
Instead, the desired expressions are likely the following:

::

     (1 + 1) .. 10
     (-1) .. 10

.. _sssec:interval_byop:

By Operator
^^^^^^^^^^^

The by operator produces an ``integer`` ``vector`` from an ``interval``.
The ``integer`` value to the right of the ``by`` operator represents an
increment between elements in the resulting ``vector``. Values are
selected beginning with and including the lower bound of the
``interval``. Values after that are obtained by adding the increment to
the previous value and appended to the resulting vector if it is less
than or equal to the upper bound of the ``interval``. For this reason,
increments of zero or less are illegal. Such an increment will
infinitely append values or cause an underflow. For example:

================= ================
``by`` expression integer vector
================= ================
``3..6 by 1``     ``[3, 4, 5, 6]``
``3..6 by 2``     ``[3, 5]``
``3..6 by 3``     ``[3, 6]``
``3..6 by 4``     ``[3]``
================= ================
