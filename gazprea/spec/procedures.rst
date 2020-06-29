.. _sec:procedure:

Procedures
==========

A procedure in *Gazprea* is like a function, except that it does not
have to be pure and as a result it may:

-  Have arguments marked with var which can be mutated. By default
   arguments are ``const`` just like functions.

-  A procedure may only accept a literal or expression as an argument if
   and only if the procedure declares that argument as ``const``

-  Procedures may perform I/O.

-  A procedure can call other procedures.

-  Procedures can only be called in assignment statements / procedure
   call statements.

-  When used in an assignment statement the procedure may only be used
   with unary operations.

Aside from this (and the different syntax necessary to declare / define
them), procedures are very similar to functions. The extra capabilities
that procedures have makes them harder to reason about, test, and
optimize.

.. _ssec:procedure_syntax:

Syntax
------

Procedures are almost exactly the same as functions, however the returns
clause is optional. Since procedures can cause side effects, it makes
sense to have procedures without a return value. If a returns clause is
present, then a return statement must be reached by all possible control
flows in the procedure before the end of the procedure is encountered.
For instance:

::

         procedure change_first(var integer vector v) {
           v[1] = 7;
         }

         procedure increment(var integer x) {
           x = x + 1;
         }

         procedure fibonacci(var integer a, var integer b) returns integer {
           integer c = a + b;
           a = b;
           b = c;
           return c;
         }

These procedures can be called as follows:

::

         integer x = 12;
         integer y = 21;
         integer vector v[5] = 13;

         call change_first(v); /* v == [7, 13, 13, 13, 13] */
         call increment(x); /* x == 13 */
         call fibonacci(x,y); /* x == 21 and y == 34 */

It is only possible to call procedures in this way. Functions must
appear in expressions because they can not cause side effects, so using
a function as a statement would not do anything, and thus *Gazprea*
should raise an error. If the procedure has a return value and is called
in this fashion the return value is discarded.

Procedures may also be called in expressions just like functions, but
with a few more limitations. A procedure may never be called within a
function, doing so would allow for impure functions. Procedures may only
be called within assignment statements (procedures may not be used as
the control expression in control flow expressions, for instance). The
return value from a procedure call can only be manipulated with unary
operators. It is illegal to use the results from a procedure call with
binary expressions, for instance:

::

         /* p is some procedure with no arguments */
         var x = p(); /* Legal */
         var y = -p(); /* Legal, depending on the return type of p */
         var z = not p(); /* Legal, depending on the return type of p */
         var u = p() + p(); /* Illegal */

This restriction is made by ``Gazprea`` in order to allow for more
optimizations.

As long as they have an appropriate return type. The difference is that
functions can be called within other functions, but procedures can not
be used within functions since procedures may be impure. Procedures may
only be called within procedures.

.. _ssec:procedure_fwd_declr:

Forward Declaration
-------------------

Procedures can use :ref:`forward declaration just like functions <ssec:function_fwd_declr>`.

.. _ssec:procedure_main:

Main
----

Execution of a *Gazprea* program starts with a procedure called
``main``. This procedure takes no arguments, and has an integer return
type. If a program is missing a main procedure an error should be
raised.

::

         /* must be writen like this */
         procedure main() returns integer {
           var out = std_output();
           integer x = 1;
           x = x + x;
           x -> out;

           /* must have a return */
           return 0;
         }

.. _ssec:procedure_alias:

Aliasing
--------

Since procedures can have mutable arguments, it would be possible to
cause `aliasing <http://en.wikipedia.org/wiki/Aliasing_(computing)>`__.
In *Gazprea* aliasing of mutable variables is illegal (the only case
where any aliasing is allowed is that tuple members can be accessed by
name, or by number, but this is easily spotted). This helps *Gazprea*
compilers perform more optimizations. However, the compiler must be able
to catch cases where mutable memory locations are aliased, and an error
should be raised when this is detected. For instance:

::

         procedure p(var integer a, var integer b, const integer c, const integer d) {
            /* Some code here */
         }

         procedure main() returns integer {
           integer x = 0;
           integer y = 0;
           integer z = 0;

           /* Illegal */
           call p(x, x, x, x); /* Aliasing, this is an error. */
           call p(x, x, y, y); /* Still aliasing, error. */
           call p(x, y, x, x); /* Argument a is mutable and aliased with c and d. */

           /* Legal */
             call p(x, y, z, z);
             /* Even though 'z' is aliased with 'c' and 'd' they are
             both const. */

           return 0;
         }

Whenever a procedure has a mutable argument x it must be checked that
none of the other arguments given to the procedure are x. This is simple
for scalar values, but more complicated when variable vectors and
matrices are passed to procedures. For instance:

::

         call p(v[1..5], v[6..10]);
         /* p is some procedure with two variable vector arguments */

In this case the arguments technically wouldn’t be aliased, since the
vector slices represent different locations in memory, but since the
vector slices may depend upon variables:

::

         call p(v[x], v[y]);
         /* p is some procedure with two variable vector arguments */

It is impossible to tell whether or not these overlap at compile time
due to the halting problem. Thus for simplicity, whenever a vector or a
matrix is passed to a procedure *Gazprea* detects aliasing whenever the
same vector / matrix is used, regardless of whether or not the sections
used would overlap. Thus, this should cause an error to be raised:

::

         call p(v[1..5], v[6..10]);
         /* p is some procedure with two variable vector arguments */


.. _ssec:procedure_vec_mat:

Vector and Matrix Parameters and Returns
----------------------------------------

:ref:`As with functions <ssec:function_vec_mat>`, the arguments and return value of procedures can have both explicit and inferred sizes.