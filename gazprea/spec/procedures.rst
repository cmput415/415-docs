.. _sec:procedure:

Procedures
==========

A procedure in *Gazprea* is like a function, except that it does not
have to be :term:`pure <functional purity>` and as a result it may:

-  Have arguments marked with ``var`` that can be mutated. By default
   arguments are ``const`` just like functions (see :ref:`sec:typeQualifiers`);
   only a ``var`` parameter may be assigned to, and a procedure that assigns to
   a ``const`` (non-``var``) parameter must emit an ``AssignError`` (see
   :ref:`sec:errors`).

-  Accept a literal or expression as an argument if and only if the
   corresponding parameter is declared ``const``.

-  Perform I/O.

-  Call other procedures.

In exchange for these capabilities, the ways in which a procedure *call* may be
used are restricted.

.. _ssec:procedure_call_positions:

A procedure call may appear only in one of three positions:

-  on the right-hand side of a declaration statement,

-  on the right-hand side of an assignment statement, or

-  as the procedure being called in a ``call`` statement.

This is the authoritative list of those positions. If you identify a
contradiction in the specification, please open an issue as that is a
specification error. A procedure call
may not be used as the control expression of a control-flow statement. The
"right-hand side of an assignment" is a *single*-target assignment or
declaration: a procedure that returns a ``tuple`` is bound to one variable first
(``var t = p();``), and it may **not** appear directly as the source of a
:ref:`tuple-unpacking assignment <sec:statements>` such as ``a, b = p();``. To
destructure the result, unpack the bound variable instead (``a, b = t;``).

Argument position is deliberately **not** on this list: a procedure call may
not appear as an argument to either a procedure call nor to
a function call. Nesting a procedure call as an argument, as in ``call
foo(p())`` or ``f(p())`` where ``p()`` is a procedure call, is
:term:`ill-formed`, and the compiler must emit a ``CallError`` (see
:ref:`sec:errors`). When programming in gazprea, the user should assign the
inner call's result to a temporary and pass that
instead. Only procedure calls are restricted this way. A *function* call
carries no such restriction and may be nested freely as an argument (subject to
the usual rule that a procedure argument may itself be a function call, but not
a procedure call).

When a procedure call appears in one of these positions, the only operations
that may be applied to its result are unary operators and
:ref:`casts <sec:typeCasting>`. The result may additionally not appear as a
component or operand inside an aggregate constructor -- an array, matrix,
tuple, or ``struct`` literal. To build an aggregate from a call's result, bind
the result to a variable first and use that variable, exactly as in the
constexpr case where ``[10, get_val()]`` is rejected (see
:ref:`ssec:constexpr_aggregates`). A procedure call used outside these
positions, or with any other
operation applied to its result, is :term:`ill-formed`; the compiler must emit
a ``CallError`` (see :ref:`sec:errors`).

Aside from this (and the different syntax necessary to declare/define
them), procedures are very similar to functions. The extra capabilities
that procedures have make them harder to reason about, test, and
optimize.

.. _ssec:procedure_syntax:

Syntax
------

Procedures are almost exactly the same as functions. However, because
procedures can cause side effects, the returns clause is optional. Due to
this, the ``= <stmt>;`` declaration format is not available for
procedures. For example, the following code is :term:`ill-formed`, and the
compiler must emit a ``SyntaxError`` (see :ref:`sec:errors`):

.. gazprea-example::
   :name: procedure_no_expr_form
   :error: SyntaxError

   procedure f() returns integer = 1;


If a returns clause is present, then a return statement must be reached
by all possible control flows in the procedure before the end of the
procedure is encountered; if control can reach the end of the body without
executing a ``return``, the compiler must emit a ``ReturnError`` (see
:ref:`sec:errors`), exactly as for :ref:`functions <sec:function>`. For
instance:

.. gazprea-example::
   :name: procedure_call_examples

   procedure change_first(var integer[*] v) {
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

   procedure main() returns integer {
     // These procedures can be called as follows:
     var integer x = 12;
     var integer y = 21;
     var integer[5] v = 13;

     call change_first(v); /* v == [7, 13, 13, 13, 13] */
     call increment(x); /* x == 13 */
     call fibonacci(x,y); /* x == 21 and y == 34 */

     v -> std_output; '\n' -> std_output;
     x -> std_output; '\n' -> std_output;
     y -> std_output;
     return 0;
   }

   --- output ---
   [7 13 13 13 13]
   21
   34

Only procedures may be called with ``call``. Functions must
appear in expressions because they cannot cause side effects, so using
a function in a ``call`` statement would not do anything. *Gazprea*'s
compiler must emit a ``CallError`` (see :ref:`sec:errors`) if a
function is used in a ``call`` statement.

.. note
   Since procedures may have no return value, it can be useful to define the
   ``void`` type even if this is its only use.

A procedure may never be called within a function, with one exception: a
mutating :ref:`vector/string method <sssec:vec_methods>` (``push``, ``append``)
may be called on a variable local to the function. Any other procedure call
within a function would allow for impure functions, and the compiler must emit
a ``CallError`` (see :ref:`sec:errors`). The positions in which a procedure
call may appear are exactly :ref:`those listed at the start of this chapter
<ssec:procedure_call_positions>`.

A procedure call may not be
used as the control expression of a control-flow statement. As noted above, the
only operations permitted on the result of a procedure call are unary operators
and :ref:`casts <sec:typeCasting>`; using the result of a procedure call in a
binary expression is :term:`ill-formed`. For example:

::

         /* p is some procedure with no arguments */
         var x = p(); /* Legal */
         var y = -p(); /* Legal, depending on the return type of p */
         var z = not p(); /* Legal, depending on the return type of p */
         var u = p() + p(); /* Illegal */

These restrictions are made by *Gazprea* arbitrarily.

Procedures without a return clause may not be used in an expression.
The compiler must emit a ``CallError`` in such a case.

.. gazprea-example::
   :name: procedure_no_return_in_expr
   :error: CallError

   /* p is some procedure with no return clause */
   procedure p() { }

   procedure main() returns integer {
     integer x = p(); /* Illegal */
     return 0;
   }

.. _ssec:procedure_fwd_declr:

Prototypes
----------

Procedures can use :ref:`forward declaration <ssec:function_fwd_declr>`
just like functions. As with a function, a procedure prototype is only a
forward *declaration* and must be matched by a definition elsewhere in the
program; a procedure that is prototyped but never defined is :term:`ill-formed`,
and the compiler must emit a ``DefinitionError`` (see :ref:`sec:errors`).

.. _ssec:procedure_main:

Main
----

Execution of a *Gazprea* program starts with a procedure called ``main``. This
procedure takes no arguments, and has an integer return type. ``main`` is
called exclusively by the operating system, and the return value is used by the
operating system, so if you are using multiple compilation units one and only
one compilation unit must define ``main``. A program with no ``main``, or whose
``main`` does not match this signature, is :term:`ill-formed` and the compiler
must emit a ``MainError`` (see :ref:`sec:errors`).

.. gazprea-example::
   :name: procedure_main

   /* must be written like this */
   procedure main() returns integer {
     var integer x = 1;
     x = x + x;
     x -> std_output;

     /* must have a return */
     return 0;
   }

   --- output ---
   2

.. _ssec:procedure_implicit_casts:

Implicit Casts of Arguments
---------------------------

An argument may be :ref:`implicitly cast <sec:implicitCasts>` to the parameter
type at call time, but only if the argument is ``const``.
A mutable (``var``) parameter the argument denote the same :term:`lvalue`
(a pointer). There is no separate value to convert, and so no
implicit cast can be inserted.

.. gazprea-example::
   :name: procedure_var_no_implicit_cast
   :error: TypeError

   procedure byvalue(string x) returns integer {
     return length(x);
   }
   procedure byreference(var string x) returns integer {
     return length(x);
   }
   procedure main() returns integer {
     const character[3] y = ['y', 'e', 's'];

     integer size = byvalue(y); // legal
     call byreference(y);       // illegal due to qualifier

     var character[3] z = ['y', 'e', 's'];
     call byreference(z); // still illegal, no implicit casts at vararg

     return 0;
   }

In ``byvalue(y)`` the argument ``y`` is a ``character[3]`` and the parameter is
a :ref:`string <ssec:string>` -- a runtime-sized :ref:`vector <ssec:vector>` of
``character``. Because the parameter is passed by value, the *value* of ``y`` is
implicitly cast to a ``string``, and that ``string`` is what ``byvalue``
receives; the caller's array ``y`` is left unchanged.

The call ``byreference(y)`` is illegal for two independent reasons. First, the
parameter ``var string x`` is call by reference, which admits no implicit cast:
there is no distinct value to convert, only the caller's storage. Second, even
setting that aside, the argument ``y`` is ``const``, and a ``var`` parameter
cannot bind a ``const`` argument; the compiler must emit a ``TypeError`` (see
:ref:`sec:errors`).


Aliasing
--------

Since procedures can have mutable arguments, it would be possible to cause
`aliasing <http://en.wikipedia.org/wiki/Aliasing_(computing)>`__. Aliasing is
restricted only when at least one of the aliased arguments is bound to a
``var`` parameter; two arguments bound to ``const`` parameters may always
alias, since neither grants the ability to mutate. A program that aliases two
such arguments, where at least one is bound to a ``var`` parameter, is
:term:`ill-formed`. This helps *Gazprea* compilers perform more aggressive
optimizations.
However, the compiler must be able to catch cases where mutable memory
locations are aliased, and must emit an ``AliasingError`` (see
:ref:`sec:errors`) when this is detected. ``AliasingError`` is always a
:term:`compile-time <compile time>` diagnosis: since exact overlap is
undecidable, the check uses the conservative *same-backing-array* rule: two
arguments that name the same array are treated as aliasing even when their
accessed ranges are disjoint. For instance:

.. gazprea-example::
   :name: procedure_aliasing_illegal
   :error: AliasingError

   procedure p(var integer a, var integer b, const integer c, const integer d) {
      /* Some code here */
   }

   procedure main() returns integer {
     var integer x = 0;
     var integer y = 0;

     call p(x, x, x, x); /* Aliasing, this is an error. */
     call p(x, x, y, y); /* Still aliasing, error. */
     call p(x, y, x, x); /* Argument a is mutable and aliased with c and d. */

     return 0;
   }

The same shape of call is legal when every aliased argument is bound to a
``const`` parameter, since neither can be mutated:

.. gazprea-example::
   :name: procedure_aliasing_legal

   procedure p(var integer a, var integer b, const integer c, const integer d) {
      /* Some code here */
   }

   procedure main() returns integer {
     var integer x = 0;
     var integer y = 0;
     var integer z = 0;

     /* Even though 'z' is aliased with 'c' and 'd' they are both const. */
     call p(x, y, z, z);

     return 0;
   }

Whenever a procedure has a mutable argument ``x`` it must be checked that
none of the other arguments given to the procedure are ``x``.
This is simple for scalar values, but more complicated when variable arrays are
passed to procedures. For instance:

::

         call p(v[x], v[y]);
         /* p is some procedure with two variable array arguments */

It is impossible to tell whether or not these overlap at :term:`compile time`
due to the halting problem. Thus for simplicity, whenever an array is passed
to a procedure *Gazprea* detects aliasing whenever the same array is used,
regardless of whether or not the access would overlap; the backing array is the
unit of aliasing. A :ref:`slice <sssec:array_slices>` is never itself a ``var``
argument -- in argument position a slice is an :term:`rvalue`, exactly like an
array literal, and binds only to a ``const`` parameter -- so a slice is not a
source of ``var``-argument aliasing.

Another instance of aliasing relates to tuple and struct fields. Passing the
same field to two ``var`` parameters is aliasing, but passing two *disjoint*
fields of the same tuple or struct to two ``var`` parameters is legal, since
disjoint fields occupy non-overlapping storage:

::

         procedure p(var integer x, var integer y) {
            /* Some code here */
         }

         var tuple(integer, integer) t = (1, 2);

         call p(t.1, t.2); /* Legal: disjoint fields, no aliasing. */
         call p(t.1, t.1); /* AliasingError: the two var arguments alias. */

.. _ssec:procedure_vec_mat:

Composite Type Parameters
-------------------------

:ref:`As with functions <ssec:function_vec_mat>`, the parameters and return
value of a procedure can have both explicit and inferred sizes, and the same
checking rules apply:

-  An explicitly sized array parameter such as ``real[3][3]`` makes that size
   part of the procedure's signature; the corresponding argument must match it
   in every dimension, or the compiler must emit a ``SizeError`` (see
   :ref:`sec:errors`).

-  An inferred-size array parameter such as ``integer[*]`` is
   :term:`initialized <initialization>` at the call from the argument that is
   passed, taking on that argument's length for the duration of the call. An
   inferred-size return type is likewise initialized at the ``return``, from the
   value being returned.

-  A :ref:`vector <ssec:vector>` parameter or return type carries no length in
   its type, so no length check applies in either direction.

Slices can be passed wherever a procedure declares a ``const`` array parameter
(see :ref:`sssec:array_slices`). Unlike functions, an array parameter of a
procedure may also be ``var``, allowing the whole array passed to it to be
modified by reference (see :ref:`ssec:procedure_mutation`).

In argument position a slice is an ordinary array **value** -- exactly like an
array literal -- so it is passed **by value**: the callee receives a *copy* of
the selected elements and cannot reach the caller's array through it, and no
aliasing arises. Because it is a value (an :term:`rvalue`), a slice binds only to
a ``const`` parameter; it may **not** be passed to a ``var`` parameter, just as
an array literal may not, and a program that does so is :term:`ill-formed`, with
the compiler emitting a ``TypeError`` (see :ref:`sec:errors`). A whole array
variable, by contrast, is an :term:`lvalue` and may bind to a ``var`` parameter.
An implementation may still pass a ``const`` slice by reference for efficiency --
because the callee only reads it, the choice is unobservable, and *Gazprea*'s
value semantics (realized directly by *MLIR*) make the copy and the shared
reference indistinguishable.

.. _ssec:procedure_mutation:

Mutating Array and Vector Parameters
----------------------------------------

A ``var`` parameter must be implemented as call by reference,
so a procedure may change what the
caller sees through it. What may change depends on whether the parameter is an
array or a vector:

-  A ``var`` array parameter is mutable in its **contents only**. Because an
   array is :ref:`initialization-time sized <sssec:array_sizing>`, a procedure
   cannot change the length of an array it was passed. Assigning a value of the
   same length replaces the contents; a shorter value is padded with the
   element type's :term:`zero value`; a longer value raises a ``SizeError``
   (see :ref:`sec:errors`).

-  A ``var`` :ref:`vector <ssec:vector>` parameter is runtime-sized and so
   **may be grown**: ``push`` and ``append`` (see :ref:`sssec:vec_methods`)
   add elements, and because the parameter is call by reference the caller
   observes the new length once the call returns.

For instance, ``fill`` overwrites the contents of an array without changing its
length, while ``extend`` lengthens a vector that its caller then observes:

::

         procedure fill(var integer[*] a, integer x) {
           a = x; /* every element of a becomes x; a's length is unchanged */
         }

         procedure extend(var vector<integer> v, integer x) {
           call v.push(x); /* v grows by one element */
         }

         procedure main() returns integer {
           var integer[3] a = 0;
           var vector<integer> v = [1, 2];

           call fill(a, 7);   /* a == [7, 7, 7]; still length 3 */
           call extend(v, 3); /* v == [1, 2, 3]; caller now sees length 3 */

           return 0;
         }

Functions, by contrast, cannot mutate their parameters at all: every function
parameter is ``const``, so a function can change neither the contents nor the
length of an array, vector, or string it receives.

.. _ssec:procedure_namespacing:

Procedure Namespacing
---------------------

Procedure identifiers share the global variable/function/procedure namespace
with every other global identifier; see :ref:`sec:namespaces` for the full
namespacing rules, including the ``SymbolError`` raised on a collision.
