Statements
----------

In *SCalc* there are five types of statements:

-  :ref:`sssec:declaration`
-  :ref:`sssec:assignment`
-  :ref:`sssec:conditional`
-  :ref:`sssec:loop`
-  :ref:`sssec:print`

Each statement ends with a semicolon. White space is not important in
*SCalc*.

**Assertion:** Whitespace is guaranteed to be a space, a tab, a carriage
return, or a new line. (:ref:`simple-whitespace <assert:simple-whitespace>`)

.. _sssec:declaration:

Declaration
~~~~~~~~~~~

A variable declaration in *SCalc* has the following form:

::

     int <id> = <expr>;

-  ``id`` is the identifier of a variable.

-  ``expr`` is an expression.

.. _variable-props:

Variables have a few properties:

-  cannot be used before being declared.

-  cannot be declared without initialisation.

-  cannot be declared more than once in an *SCalc* program.

Examples of valid declarations are:

::

     int i = 9;
     int j = 9 * 4 + 10;
     int k = i * j;

Examples of invalid declarations are:

::

     int i;
     int j =;

.. _sssec:assignment:

Assignment
~~~~~~~~~~

Variable assignment is similar to variable declaration but it allows
variables to be assigned new values. An assignment in *SCalc* has the
following form:

::

     <id> = <expr>;

-  ``id`` is the identifier of an already declared variable.

-  ``expr`` is an expression.

.. _sssec:conditional:

Conditional
~~~~~~~~~~~

A conditional in *SCalc* has the following form:

::

     if (<expr>)
       <statement-1>
       <statement-2>
       ...
       <statement-n>
     fi;

-  ``expr`` is an expression. The body of the ``if`` statement is
   executed if and only if this expression evaluates to a non-zero
   value.

-  ``statement-*`` is any type of statement *except* a declaration. This
   means there can be assignments, nested loops, nested conditionals,
   and prints. There does not have to be any statements in the
   conditional.

**Clarification:** Declarations in conditionals can lead to undefined
values due to global scoping. (:ref:`no-decl-cond <clarify:no-decl-cond>`)

.. _sssec:loop:

Loop
~~~~

A loop in *SCalc* has the following form:

::

     loop (expr)
       <statement-1>
       <statement-2>
       ...
       <statement-n>
     pool;

-  ``expr`` is an expression. The body of the ``loop`` statement is
   repeatedly evaluated as long as this expression is non-zero. The
   expression is evaluated prior to running the body similar to a *C*
   ``while`` loop.

-  ``statement-*`` is any type of statement *except* a declaration. This
   means there can be assignments, nested loops, nested conditionals,
   and prints. There does not have to be any statements in the loop, but
   without side effects a loop will be infinite (unless it is never
   entered).

**Clarification:** Declarations in loops can lead to undefined or
repeatedly defined values due to global scoping.
(:ref:`no-decl-loop <clarify:no-decl-loop>`)

.. _sssec:print:

Print
~~~~~

Print statements print the integer value of an expression followed by a
newline. A print statement in *SCalc* has the following form:

::

     print(<expr>);

-  ``expr`` is an expression.

For example, the input:

::

     int i = 0;
     loop (i < 5)
       print(i);
       i = i + 1;
     pool;

should print:

::

     0
     1
     2
     3
     4

