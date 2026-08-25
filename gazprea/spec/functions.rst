.. _sec:function:

Functions
=========

A function in *Gazprea* has several requirements:

1.  All of the arguments are implicitly ``const``, and cannot be mutable.

2.  Function arguments cannot contain type qualifiers. Including a type
    qualifier with a function argument must emit a ``SyntaxError`` (see
    :ref:`sec:errors`).

3.  Argument types must be explicit. Inferred size arrays are allowed.

4.  Functions cannot perform any I/O; performing I/O in a function body must
    emit a ``StatementError`` (see :ref:`sec:errors`).

5.  Functions cannot rely upon any mutable state outside of the function.

6.  Functions cannot call any procedures, with one exception: a mutating
    vector/string method (``push``, ``append``) may be called on a variable
    local to the function (see :ref:`sssec:vec_methods`); any other procedure
    call inside a function must emit a ``CallError`` (see :ref:`sec:errors`).

7.  Functions must be declared in the global scope.

The reason for this is to ensure that functions in *Gazprea* behave as
:term:`pure functions <functional purity>`. Every time you call a function
with the same arguments
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
         real c = pythag(3, 4); /* 3 and 4 are implicitly cast to real. c == 5.0 */
         real value = get([i in 1..10 | i], 3); /* value == 3 */

A function's body can also be given by a block statement instead of a
single expression. In this case the return value of the function is
given with the return statement. A return statement must be reached by
all possible control flows in the function before the end of the
function is encountered; if this cannot be established the compiler must
emit a ``ReturnError`` (see :ref:`sec:errors`).

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

``f`` is :term:`ill-formed` since if ``b == false``, then we reach the
end of the function without a return statement, so we do not know what
value ``f(false)`` should take on.  A conforming implementation must
emit a ``ReturnError`` (see :ref:`sec:errors`) rejecting this program, such as::

     ReturnError on line 1: function "f" does not have a return statement reachable by all control flows

::

         /* This is invalid because if the loop ever finished executing the
            function would end before a return statement is encountered. In
            general the compiler cannot tell when a loop would execute
            forever, so we make the assumption that all branches in the control
            flow could be followed. */
         function f() returns integer {
           var integer x = 0;
           loop {
             x = x + 1;
           }
         }

         /* This is valid. Even though the loop goes on forever so that a
            return is never reached, execution never hits the end of the
            function without a return. */
         function g() returns integer {
           var integer x = 0;
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
function definitions are in different source files.

::

         /* Forward declaration, no body */
         function f(integer y, integer) returns integer;

         procedure main() returns integer {
           integer y = f(13, 2);
           /* Can use this in main, even though the definition is below */
           return 0;
         }

         function f(integer x, integer z) returns integer = x*z;

Note that only the type signatures of the forward declaration of the
function and the definition must be identical. That means the argument names in
the prototype are *optional*. If the prototype arguments are given names they
do not have to match the argument names in the function definition.


.. _ssec:function_vec_mat:

Array and Matrix Parameters and Returns
----------------------------------------

The arguments and return value of functions can have both explicit and inferred
sizes. For example:

::

         function to_real_vec(integer[*] x) returns real[*] {
             /* Some code here */
         }

         function transpose3x3(real[3][3] x) returns real[3][3] {
             /* Some code here */
         }


The size written in a parameter or return type is part of how each call is
checked:

-  An **explicitly sized** array parameter such as ``real[3][3]`` makes that
   size part of the function's signature. The corresponding argument must have
   exactly that length in every dimension, or the compiler must emit a
   ``SizeError`` (see :ref:`sec:errors`).

-  An **inferred-size** array parameter such as ``integer[*]`` imposes no size
   requirement of its own. It is :term:`initialized <initialization>` at the
   call from the argument that is passed, taking on that argument's length,
   which is then fixed for the duration of the call (see
   :ref:`sssec:array_sizing`).

-  An **inferred-size return type** such as ``real[*]`` is likewise
   :term:`initialized <initialization>` at the ``return`` statement, from the
   value being returned.

-  A :ref:`vector <ssec:vector>` parameter or return type (for example
   ``vector<real>``, or the :ref:`string <ssec:string>` alias) carries no
   length in its type, so no length check applies in either direction; the
   parameter simply takes on the length of the value passed or returned.

Array *slices* may also be passed as arguments:

::

         function to_real_vec(integer[*] x) returns real[*] {
            real[*] rvec = x;
            return rvec;
         }

         function slicer() returns real[*] {
             integer[10] a = 1..11;
             var vector<real> two_halves = to_real_vec(a[1..6]);
             call two_halves.append(to_real_vec(a[6..]));
             return two_halves;
         }

Remember that all function parameters are ``const`` in *Gazprea*, so that all
functions are pure. That means that arrays, vectors, and strings, like every
other function argument, are passed *by value* at the call (see
:ref:`ssec:procedure_implicit_casts`), not by reference; a function can change
neither the contents nor the length of an array, vector, or string it
receives, since a ``const`` parameter cannot be assigned to at all. A function
that assigns to one of its parameters must emit an ``AssignError`` (see
:ref:`sec:errors`).

Because every function parameter is ``const``, an array :ref:`slice
<sssec:array_slices>` passed to a function is received **by value** -- a copy of
the selected elements -- and so can never observe or cause a change to the
slice's backing storage. The view-versus-copy distinction that matters for a
``var`` parameter therefore does not arise for functions: every slice a function
receives is a copy.

.. _ssec:function_namespacing:

Function Namespacing
--------------------

Function identifiers share the global variable/function/procedure namespace
with every other global identifier; see :ref:`sec:namespaces` for the full
namespacing rules, including the ``SymbolError`` raised on a collision.
