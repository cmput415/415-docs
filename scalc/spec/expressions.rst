Expressions
-----------

An expression is composed of integers, identifiers, and operators.

Operators
~~~~~~~~~

Operators are listed in descending precedence order. Operators without a
horizontal line dividing them have equal precedence. For example,
addition and subtraction have an equal level of precedence.

========== ============== ========== ================ =================
**Class**  **Operation**  **Symbol** **Usage**        **Associativity**
========== ============== ========== ================ =================
Arithmetic multiplication \*         ``expr * expr``  left
\          division       /          ``expr / expr``  left
\          addition       +          ``expr + expr``  left
\          subtraction    -          ``expr - expr``  left
Comparison less than      <          ``expr < expr``  left
\          greater than   >          ``expr > expr``  left
\          is equal       ==         ``expr == expr`` left
\          is not equal   !=         ``expr != expr`` left
========== ============== ========== ================ =================

| **Clarification:** There is no remainder operator in SCalc.
  (:ref:`no-rem <clarify:no-rem>`)
| **Clarification:** There is no exponentiation operator in SCalc.
  (:ref:`no-pow <clarify:no-pow>`)
| **Clarification:** Division is integer division.
  (:ref:`int-div <clarify:int-div>`)

Valid Expressions
~~~~~~~~~~~~~~~~~

Valid formats for expressions are

::

     (<expr>)
     <expr> <op> <expr>
     <int>
     <id>

-  ``expr`` is an expression.

-  ``int`` is an integer.

-  ``id`` is the identifier of a variable.

| **Assertion:** All expressions will result in a value that fits in a
  32 bit signed integer. (:ref:`expression-size <assert:expression-size>`)
| **Assertion:** No expression will contain a division by 0.
  (:ref:`zero-divide <assert:zero-divide>`)

Examples of valid expressions are

::

     i * 2 * 10 + 4
     2 - 4 * 5

Precedence
~~~~~~~~~~

Precedence determines what order operations are evaluated in. Precedence
works as defined in the following table:

============== ==============
**Precedence** **Operations**
============== ==============
HIGHER         \*,/
\              +,-
\              <, >
LOWER          ==, !=
============== ==============

