Variables
=========

Scope
~~~~~

All variable scope is local to the main program block.
Variables are only accessible after declaration, and there is no global scope.

Naming
~~~~~~

Variable identifiers may be in all uppercase or lowercase letters (or a mixture of the two). They must begin with a letter and may be followed only by other letters, numbers, and underscores. No spaces, dashes, or other symbols are allowed. Variable identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and "CHEEZBURGER" would all be different variables.

Types
~~~~~

For the purposes of this assignment, LOLCODE recognizes four types, though only three of them can be declared as variables:

- **YARN** or strings. Literals are enclosed in double quotes ('"') at each end. We are not going to try to support escape characters for this assignment.

- **NUMBR** or integers. Integers can be represented using the host's 32-bit implementation. Integer literals are allowed to have a leading hyphen ('-') to signify a negative number.

- **TROOF** or boolean, where true is WIN and false is FAIL. TROOF is a value type produced by comparisons (``BOTH SAEM``, ``DIFFRINT``) and consumed by conditionals (``O RLY?``, ``MEBBE``), but it cannot be declared as a variable or cast to with MAEK in this reduced version of the language.

- **NOOB** or void. This is the type given to uninitialized variables.

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
Assignment of a variable is accomplished with an assignment statement, ``<variable> R <expression>``

::

    I HAS A VAR            BTW VAR is null and type NOOB
    VAR R "THREE"          BTW VAR is now a YARN and equals "THREE"
    VAR R 3                BTW VAR is now a NUMBR and equals 3

