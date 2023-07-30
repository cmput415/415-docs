.. _sec:statements:

Statements
==========

.. _ssec:statements_assign:

Assignment Statements
---------------------

In *Gazprea* a variable may have different values throughout the
execution of the program. Variables may have their values changed with
an assignment statement. In the simplest case an assignment statement
contains an identifier on the left hand side of an equals sign, and an
expression with a compatible type on the right hand side.

::

         integer x = 7;

         x -> std_output;  /* Prints 7 */

         /* Give 'x' a new value */
         x = 2 * 3;  /* This is an assignment statement */

         x -> std_output;  /* Prints 6 */

Type checking must be performed on assignment statements. The expression
on the right hand side must have a type that can be automatically
promoted to the type of the variable. For instance:

::

         integer int_var = 7;
         real real_var = 0.0;
         boolean bool_var = true;

         /* Since 'x' is an integer it can be promoted to a real number */
         real_var = int_var;  /* Legal */

         /* Real numbers can not be turned into boolean values automatically. */
         bool_var = real_var; /* Illegal */

Assignments can also be more complicated than this with vectors,
matrices, and tuples. With matrices and vectors indices may be provided
in order to change the value of a portion of the matrix or vector. For
instance, with vectors:

::

         integer[*] v = [0, 0, 0];

         /* Can assign an entire vector value -- change 'v' to [1, 2, 3] */
         v = [1, 2, 3];

         /* Change 'v' to [1, 0, 3] */
         v[2] = 0;

         /* Can also use vector indexing */
         v[[1, 3]] = [4, 5];  /* 'v' is now [4, 0, 5] */

         integer[*] w = [3, 2, 1];

         /* Also note this special case */
         w[w] = [2, 2, 2]; /* 'w' is now [3, 2, 2] */
         // The above assignment is semantically equivalent to the following loop
         loop i in 1..3 {
             w[w[i]] = 2;
         }

Matrices can be treated similarly.

::

         integer[*, *] M = [[1, 1], [1, 1]];

         /* Change the entire matrix M to [[1, 2], [3, 4]] */
         M = [[1, 2], [3, 4]];

         /* Change a single position of M */
         M[1, 2] = 7;  /* M is now [[1, 7], [3, 4]] */

         /* Can use vector indexing on rows or columns.
            Uses all combinations of row / column coordinates */

Tuples also have a special unpacking syntax in *Gazprea*. A tuple’s
field may be assigned to comma separated variables instead of a tuple
variable. For instance:

::

         integer x = 0;
         real y = 0;
         real z = 0;

         tuple(integer, real) tup = (1, 2.0);

         /* x == 1, and y == 2.0 now */
         x, y = tup;

         /* Types can be promoted */

         /* z == 1.0, y == 2.0 */
         z, y = tup;

         /* Can swap: z == 2.0, y == 1.0 */
         z, y = (y, z);

The types of the variables must match the types of the tuple’s fields,
or the tuple’s fields must be able to be automatically promoted to the
variable’s type. The number of variables in the comma separated list
must match the number of fields in the tuple, if this is not the case an
error should be raised.

Assignments and initializations must perform a deep copy. It should not
be possible to cause the aliasing of memory locations with an
assignment. For instance:

::

         integer[*] v = [1, 2, 3];
         integer[*] w = v;

         w[2] = 0;  /* This must not affect 'v' */

         /* v has the value [1, 2, 3] */
         /* w has the value [1, 0, 3] */

         /* If you are not careful, you might copy the pointer of 'v' to 'w',
            which would cause them to be stored in the same location in memory. If
            this happens modifying 'w' would change 'v' as well.
          */

The above is a simple example using vectors. You must ensure that values
can not be aliased with an assignment between any types, including
vectors, matrices, and tuples.

Variables may be declared as const, and in this case it is illegal for
them to appear on the left hand side of an assignment expression. The
compiler should raise on error when this is detected, since it does not
make sense to change a constant value.

The right hand side of an assignment statement is always evaluated
before the left hand side. This is important for cases where procedures
may change variables, for instance:

::

         v[x] = p(x);
         /* If p changes x then it is important that p(x) is executed before v[x] */

.. _ssec:statements_block:

Block Statements
----------------

A list of statements may be grouped into one statement using curly
braces. This is called a block statement, and is similar to block
statements in other languages such as *C/C++*. As an example:

::

         {
           x = 3;
           z = 4;
           x -> std_output; "\n" -> std_output; z -> std_output; "\n" -> std_output;
         }

Is a block statement. Declarations can only appear at the start of a
block. Each block statement introduces a new scope that new variables
may be declared in. For instance this is perfectly valid:

::

         integer x = 3;
         integer y = 0;
         real z = 0;

         {
           real x = 7.1;
           z = x;
         }

         y = x;

After execution this ``y = 3`` and ``z = 7.1``.

.. _ssec:statements_cond:

If/Else Statements
------------------

An if statement takes a boolean value as a conditional expression, and a
statement for the body. If the conditional expression evaluates to true,
then the body is executed. If the conditional expression evaluates to
false then the body of the if statement is not executed. If statements
in *Gazprea* do not require the conditional expression to be enclosed in
parenthesis.

::

         integer x = 0;
         integer y = 0;

         /* Compute some value for x */

         if (x == 3) {
            y = 7;
         }

         /* At this point y will only be 7 if x == 3, and otherwise y will be
            0, assuming it did not change throughout the rest of the program.
          */

If statements are often paired with block statements, like in the above
example. The if statement above could also be written as:

::

         if x == 3
           y = 7;

Since ``y = 7;`` is a statement it can be used as the body statement.
All statements after this point are not in the body of the if statement.
For instance:

::

         if x == 3
           y = 7;
           z = 32;

is actually equivalent to the following:

::

         if (x == 4) {
           y = 7;
         }

         z = 32;

*Gazprea* is not sensitive to whitespace, so we could even write
something like:

::

         if x == 3 y = 7;

An if statement may also be followed by an else statement. The else has
a body statement just like the if statement, but this is only run if the
conditional expression on the if statement fails.

::

         if x == 3
           y = 7;
         else
           y = 32;

Now if ``x`` does not have a value of 3, ``y`` is assigned a value of
32. This can be paired with if statements as well.

::

         y = 0;

         if (x < 0) {
           y = -1;
         }
         else if (x > 0) {
           y = 1;
         }

         /* y is negative if x is negative, positive if x is positive,
           and 0 if x is 0. */

.. _ssec:statements_loop:

Loop
----

.. _sssec:statements_inf_Loop:

Infinite Loop
~~~~~~~~~~~~~

*Gazprea* provides an infinite loop, which continuously executes the
body statement given to it. For instance:

::

           loop "hello!\n" -> std_output;

Would print "hello!" indefinitely. This is often used with block
statements.

::

           /* Infinite counter */
           integer n = 0;

           loop {
             n -> std_output; "\n" -> std_output;
             n = n + 1;
           }

.. _sssec:statements_pred_loop:

Predicated Loop
~~~~~~~~~~~~~~~

A loop may also be provided with a control expression. The control
expression automatically breaks from the loop if it evaluates to false
when it is checked.

The loop can be pre-predicated, which means that the control expression
is tested before the body statement is executed. This is the same
behaviour as while loops in most languages, and is written using the
``while`` token after the ``loop``, followed by a boolean expression for the
predicate. For example:

::

           integer x = 0;

           /* Print 1 to 10 */
           loop while x < 10 {
             x = x + 1;
             x -> std_output; "\n" -> std_output;
           }

A post-predicated loop is also available. In this case the control
expression is tested after the body statement is executed. This also
uses the ``while`` token followed by the control expression, but it appears
at the end of the loop. Post Predicated loop statements must end in a
semicolon.

::

           integer x = 10;

           /* Since the conditional is tested after the execution '10' is printed */
           loop x -> std_output; while x == 0;

.. _sssec:statements_iter_loop:

Iterator Loop
~~~~~~~~~~~~~

Loops can be used to iterate over the elements of an integer interval,
or a vector of any type. This is done by using domain expressions (for
instance ``i in v``) in conjunction with a loop statement.

When the domain is given by a vector, each time the loop is executed the
next element of the vector is assigned to the domain variable. The
elements of the domain vector are assigned to the domain variable
starting from index 1, and going up to the final element of the vector.
When all of the elements of the domain vector have been used the loop
automatically exits. For instance:

::

           /* This will print 123 */
           loop i in [1, 2, 3] {
             i -> std_output;
           }

Integer intervals can also be used instead. In this case it is the same
as iterating over a vector created from the interval using ``by 1``. For
instance, the above iterator loop is equivalent to the following:

::

           /* This will print 123 */
           loop i in 1..3 {
             i -> std_output;
           }

The domain is evaluated once during the first iteration of the loop. For
instance:

::

           integer[*] v = [i in 1..3 | i];

           /* Since the domain 'v' is only evaluated once this loop prints 1, 2,
              and then 3 even though after the first iteration 'v' is the zero
              vector. */
           loop i in v {
             v = 0;
             i -> std_output; "\n" -> std_output;
           }

Multiple domain expressions may be used by separating them with commas.

::

           loop i in u, j in v {
             "Hello!\n" -> std_output;
           }

           /* The above loop is equivalent to the loop below */

           loop i in u {
             loop j in v {
               "Hello!\n" -> std_output;
             }
           }

This can be done with as many domain expressions as desired.

.. _ssec:statements_break:

Break
-----

A ``break`` statement may only appear within the body of a loop. When a
``break`` statement is executed the loop is exited, and *Gazprea* continues
to execute after the loop. This only exits the innermost loop, which
actually contains the ``break``.

::

         /* Prints a 3x3 square of *'s */
         integer x = 0;
         integer y = 0;

         loop while y < 3 {
           y = y + 1;

           /* Normally this would loop forever, but the break exits this inner loop */
           loop {
             if x >= 3 break;

             x = x + 1;
             "*" -> std_output;
           }

           "\n" -> std_output;
         }

If a ``break`` statement is not contained within a loop an error must be
raised.

.. _ssec:statements_continue:

Continue
--------

Similarly to ``break``, ``continue`` may only appear within the body of
a loop. When a ``continue`` statement is executed the innermost loop
that contains the ``continue`` statements starts its next iteration.
``continue`` stops the execution of the loop’s body statement, the loop
then continues as though the body statement finished its execution
normally.

::

         /* Prints every number between 1 and 10, except for 7 */
         integer x = 0;

         loop while x < 10 {
           x = x + 1;

           if x == 7 continue;  /* Start at the beginning of the loop, skip 7 */

           x -> std_output; "\n" -> std_output;
         }

.. _ssec:statements_return:

Return
------

The ``return`` statement is used to stop the execution of a function or
procedure. When a function/procedure returns then execution continues where the
function/procedure was called.

If the function/procedure has a return type then the ``return`` statement must
be given a value that is the same as or able to be promoted to (see
:ref:`sec:typePromotion`) the return type; this will be the result of the
function/procedure call. Here is an example:

::

  function square(integer x) returns integer {
    return x * x;
  }

If a procedure has no ``returns`` clause, then it has no return type and a
``return`` statement is not required but may still be present in order to
return early. In this case return is used as follows:

::

  procedure do_nothing() {
    return;
  }

.. _ssec:statements_streams:

Stream Statements
-----------------

Stream statements are the statements used to read and write values in
*Gazprea*.

Output example:

::

         2 * 3 -> std_output;  /* Prints 6 */

Input example:

::

         integer x = null;
         x <- std_input; /* Read an integer into x */
