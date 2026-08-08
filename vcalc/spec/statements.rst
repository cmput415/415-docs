Statements
----------

Declaration
~~~~~~~~~~~

A variable declaration in *VCalc* has the following form:

::

     <type> <id> = <expr>;

-  ``<type>`` is the type of the variable: ``int`` or ``vector``.

-  ``<id>`` is the identifier of a variable.

-  ``<expr>`` is an expression.

.. _variable-props:

Variables have a few properties:

-  cannot be used before being declared.

-  cannot be declared without initialisation.

-  cannot be declared more than once in a *VCalc* program.

Examples of valid declarations are:

::

     int i = 9;
     int j = 9 * 4 + 10;
     vector k = i..j;

Examples of invalid declarations are:

::

     int i;
     vector j =;

Vectors may be initialized with any expression
that returns a vector. For example, assigning a range to a vector ``v``:

::

     vector v = 1..10;
     print(v);

prints the following:

::

     [1 2 3 4 5 6 7 8 9 10]

.. _sssec:assignment:

Assignment
~~~~~~~~~~

Variable assignment is similar to variable declaration but it allows
variables to be assigned new values. An assignment in *VCalc* has the
following form:

::

     <id> = <expr>;

-  ``id`` is the identifier of an already declared variable.

-  ``expr`` is an expression.

There are a few new important points when dealing with assignments.

#. The size of a vector may change while the program is executing if a
   vector variable is assigned another value. For instance, the
   following sequence of statements *is* valid:

   ::

            vector v = 1..10;
            v = 1..1000;

   You will have to allocate more memory to store the result of the
   assignment.

#. The type of the expression of the assignment must match the
   destination variable’s type. This is apparent for trying to assign
   vectors to a scalar. In the case of scalars being assigned to
   vectors, one might expect that we can use our extension policy to
   copy our scalar to every index of a newly created vector but the
   question is, how large is the new vector. Because that is
   indeterminable, this is not allowed. For example, the following
   sequence of statements *is not* valid:

   ::

            int i = 1..3;
            vector v = 1;

#. Many languages allow you to assign to vector indices, *VCalc does
   not*. For example, the following sequence of statements *is not*
   valid:

   ::

            vector v = 1..3;
            v[0] = 99;

Conditional
~~~~~~~~~~~

A conditional in *VCalc* has the following form:

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

- conditional conditions must evaluate to booleans, which means that vectors
  are not a valid condition. Remember, however, that integers can
  be implicitly downcast to booleans.

-  ``statement-*`` is any type of statement *except* a declaration. This
   means there can be assignments, nested loops, nested conditionals,
   and prints. There does not have to be any statements in the
   conditional.

**Clarification:** Declarations in conditionals can lead to undefined
values due to global scoping. (:ref:`no-decl-cond <clarify:no-decl-cond>`)


Loops
~~~~~

A loop in *VCalc* has the following form:

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

- Loop conditions must evaluate to booleans, which means that vectors are not a
  valid condition. Remember, however, that integers can be implicitly downcast
  to booleans.

-  ``statement-*`` is any type of statement *except* a declaration. This
   means there can be assignments, nested loops, nested conditionals,
   and prints. There does not have to be any statements in the loop, but
   without side effects a loop will be infinite (unless it is never
   entered).

**Clarification:** Declarations in loops can lead to undefined or
repeatedly defined values due to global scoping.
(:ref:`no-decl-loop <clarify:no-decl-loop>`)

Print
~~~~~

Print statements print the value of an expression followed by a newline.
A print statement in *VCalc* has the following form:

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


The ``print`` statement must also be able to output vectors. All the elements of
the vector are printed on a single line between the opening and closing brackets.

For example:

::

     print(1..10);

prints the following:

::

     [1 2 3 4 5 6 7 8 9 10]


The output of ``print`` is standardized to ensure everyone can pass everyone’s
tests. Follow these specifications:

-  There *must* be a new line after each ``print`` statement’s printed
   value.

-  There *must not* be any trailing space after printed value and before
   the newline.

-  There *must* be an empty line at the end of your output.

-  There *must not* be spaces between the first and last number and the
   accompanying brackets in a vector.

-  There *must* be spaces between the numbers in a vector.

-  There *must not* be anything except spaces between the numbers in a
   vector.

| **Clarification:** Empty input should result in empty output.
  (:ref:`empty-input <clarify:empty-input>`)
| **Clarification:** Empty vectors print only brackets.
  (:ref:`empty-vector <clarify:empty-vector>`)
| **Clarification:** A vector with one value is only the brackets and
  the value. (:ref:`single-value-vector <clarify:single-value-vector>`)
