.. _sec:function:

Functions
=========

A function in *Gazprea* has several requirements:

-  All of the arguments are implicitly ``const``, and can not be
   mutable.

-  Function arguments cannot contain type qualifiers. Including a type qualifier
   with a function argument should result in a ``SyntaxError``.

-  Argument types must be explicit. Inferred size vectors are allowed

-  Functions can not perform any I/O.

-  Functions can not rely upon any mutable state outside of the function.

-  Functions can not call any procedures.

-  Functions must be declared in the global scope.

The reason for this is to ensure that functions in *Gazprea* behave as
pure functions. Every time you call a function with the same arguments
it will perform the exact same operations. This has a lot of benefits.
It makes code easier to understand if functions only depend upon their
inputs and not some hidden state, and it also allows the compiler to
make more assumptions and as a result perform more optimizations.

.. _ssec:function_syntax:

Syntax
------

A function is declared using the function keyword. Each function is
given an identifier, and an arguments list enclosed in parenthesis. If
no arguments are provided an empty set of parenthesis, ``()``, must be
used. The return type of the function is specified after the arguments
using ``returns``.

A function can be given by a single expression. For instance:

::

         function times_two(integer x) returns integer = 2 * x;

This defines a function called times_two which can be used as follows:

::

         /* Prints 8. value gets assigned the result of calling times_two with an
            argument of 4
          */
         integer value = times_two(4);

         value -> std_output; "\n" -> std_output;

Functions can have an arbitrary number of arguments. Here are some
examples of functions with different numbers of arguments:
::

         /* A function with no arguments */
         function f() returns integer = 1;

         /* A function with two arguments */
         function pythag(real a, real b) returns real = (a^2 + b^2)^(1./2);

         /* A function with different types of arguments */
         function get(real[*] a, integer i) returns real = a[i];

These can be called as follows:

::

         integer x = f(); /* x == 1 */
         real c = pythag(3, 4); /* Type promotion to real arguments. c == 5.0 */
         real value = get([i in 1..10 | i], 3); /* value == 3 */

A function’s body can also be given by a block statement instead of a
single expression. In this case the return value of the function is
given with the return statement. A return statement must be reached by
all possible control flows in the function before the end of the
function is encountered.

::

         /* Invalid -- should cause a compiler error */
         function f (boolean b) returns integer {
           if (b) {
             return 3;
           }
         }

         /* Valid, all possible branches hit a return statement with a valid type */
         function g (boolean b) returns integer {
           if (b) {
             return 3;
           }
           else {
             return 8;
           }
         }

``f`` is invalid since if ``b == false``, then we reach the end of the
function without a return statement, so we don’t know what value
``f(false)`` should take on.

::

         /* This is invalid because if the loop ever finished executing the
            function would end before a return statement is encountered. In
            general the compiler can not tell when a loop would execute
            forever, so we make the assumption that all branches in the control
            flow could be followed. */
         function f() returns integer {
           integer x = 0;
           loop {
             x = x + 1;
           }
         }

         /* This is valid. Even though the loop goes on forever so that a
            return is never reached, execution never hits the end of the
            function without a return. */
         function g() returns integer {
           integer x = 0;
           loop {
             x = x + 1;
           }

           return x;
         }

Each function has its own scope, but globals can be accessed within the
function if they were declared before the function was defined.

.. _ssec:function_fwd_declr:

Function Prototypes
-------------------

Functions can be declared before they are defined in a *Gazprea* file.
This allows function definitions to be moved to more convenient
locations in the file, and allows for multiple compilation units if the
functions.

::

         /* Forward declaration, no body */
         function f(integer y, integer) returns integer;

         procedure main() returns integer {
           integer y = f(13);
           /* Can use this in main, even though the definition is below */
           return 0;
         }

         function f(integer x, integer z) returns integer = x*z;

Note that only the type signatures of the forward declaration of the
function and the definition must be identical. That means the argument names in
the prototype are *optional*. If the prototype arguments are given names they
do not have to match the argument names in the function definition.


.. _ssec:function_vec_mat:

Vector and Matrix Parameters and Returns
----------------------------------------

The arguments and return value of functions can have both explicit and inferred sizes. For example:

::

         function to_real_vec(integer[*] x) returns real[*] {
             /* Some code here */
         }

         function transpose3x3(real[3,3] x) returns real[3,3] {
             /* Some code here */
         }
