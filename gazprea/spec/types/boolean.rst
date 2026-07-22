.. _ssec:boolean:

Boolean
-------

A ``boolean`` is either ``true`` or ``false``. A ``boolean`` can be
represented by an ``i1`` in *MLIR*.

.. _sssec:boolean_decl:

Declaration
~~~~~~~~~~~

A ``boolean`` value is declared with the keyword ``boolean``.
If the variable is not initialized explicitly, it is set to ``false`` (zero).

.. _sssec:boolean_lit:

Literals
~~~~~~~~

The following are the only two valid ``boolean`` literals:

-  ``true``

-  ``false``

.. _sssec:boolean_ops:

Operations
~~~~~~~~~~

The following operations are defined on ``boolean`` values. In all
of the usage examples ``bool-expr`` means some ``boolean`` yielding
expression.

============= ========== =========================== =================
**Operation** **Symbol** **Usage**                   **Associativity**
============= ========== =========================== =================
parenthesis   ``()``     ``(bool-expr)``             N/A
negation      ``not``    ``not bool-expr``           right
logical or    ``or``     ``bool-expr or bool-expr``  left
logical xor   ``xor``    ``bool-expr xor bool-expr`` left
logical and   ``and``    ``bool-expr and bool-expr`` left
equals        ``==``     ``bool-expr == bool-expr``  left
not equals    ``!=``     ``bool-expr != bool-expr``  left
============= ========== =========================== =================

Unlike many languages the ``and`` and ``or`` operators do not `short
circuit
evaluation <https://en.wikipedia.org/wiki/Short-circuit_evaluation>`__.
Therefore, both the left hand side and right hand side of an expression
must always be evaluated.

Operator precedence and associativity are specified once, for all
types, in the :ref:`table of operator precedence
<ssec:expressions_toop>`.

Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``boolean`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` 
respectively.
