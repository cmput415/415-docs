Variables
=========

Scope
~~~~~

All variable :term:`scope` is local to the main program block.
Variables are only accessible after :term:`declaration`, and there is no
global scope.

Naming
~~~~~~

Variable :term:`identifiers <identifier>` may be in all uppercase or
lowercase letters (or a mixture of the two). They must begin with a
letter and may be followed only by other letters, numbers, and
underscores. No spaces, dashes, or other symbols are allowed. Variable
identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and
"CHEEZBURGER" would all be different variables.

Types
~~~~~

For the purposes of this assignment, LOLCODE only recognizes three
:term:`types <type>`:

- **YARN** or strings. :term:`Literals <literal>` are enclosed in double quotes ('"') at each end. We are not going to try to support escape characters for this assignment.

- **NUMBR** or integers. Integers can be represented using the host's 32-bit implementation. Integer literals are allowed to have a leading hyphen (``-``) to signify a negative number.

- **TROOF** or boolean, where true is ``WIN`` and false is ``FAIL``. Although full LOLCODE supports both variables and :term:`expressions <expression>` of type TROOF, we only include it here for reference in the the descriptions taken from the spec.

- **NOOB** or void. This is the type given to uninitialized variables. It is usually implicit, but we may refer to it in the spec.

.. _sssec:declaration:

Declaration
~~~~~~~~~~~

To declare a variable, the keyword is ``I HAS A`` followed by the variable name. To assign the variable a value within the same statement, you can then follow the variable name with ``ITZ <value>``.

::

    I HAS A VAR            BTW VAR is empty and has type NOOB
    I HAS A var ITZ 2      BTW var is type NUMBR and value 2

.. _sssec:assignment:

Assignment
~~~~~~~~~~
Assignment of a variable is accomplished with an assignment :term:`statement`, ``<variable> R <expression>``

::

    I HAS A VAR            BTW VAR is null and type NOOB
    VAR R "THREE"          BTW VAR is now a YARN and equals "THREE"
    VAR R 3                BTW VAR is now a NUMBR and equals 3


.. _sssec:cast:

Casting
~~~~~~~

Operators that work on specific types apply an :term:`implicit conversion` to parameter values of other types. If the value cannot be safely converted, then it results in an error.

An :term:`expression`'s value may undergo :term:`type casting` with the binary ``MAEK`` operator:

::

    MAEK <variable> [A] <type>

Where ``<type>`` is one of ``YARN`` or ``NUMBR``.

To explicitly re-cast a variable, you may create a normal assignment statement with the ``MAEK`` operator, or use a casting assignment statement as follows:

::

    <variable> R MAEK <variable> [A] <type>
