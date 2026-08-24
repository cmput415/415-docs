.. _sec:builtIn:

Built-In Functions
==================

*Gazprea* has some built-in functions. These built-in functions may have
some special behavior that normal functions cannot have, for instance
many of them will work on arrays of any element type.
Normally a function must specify the element type of an array argument.

The names of the built-in functions are reserved. A user program may not
declare *any* identifier -- a variable, function, procedure, ``struct``, or
otherwise -- with the same name as a built-in function; doing so would shadow
the built-in, and the compiler must emit a ``SymbolError`` (see
:ref:`sec:errors`). These names are reserved semantically rather than being
syntactic :ref:`keywords <sec:keywords>`.

The :ref:`vector/string method <sssec:vec_methods>` names (``push``,
``append``, ``len``), by contrast, are **not** reserved. They live in a method
namespace associated with the compiler-defined ``vector`` object -- reachable
only after a ``.`` on a ``vector`` receiver -- and so do not collide with the
global identifier namespace. A user may freely declare, say, a ``function
len()`` or a variable named ``push``.

Note that although the examples below all use arrays, the array-shaped
built-ins (``length``, ``reverse``) also work on
:ref:`vectors <ssec:vector>` and :ref:`strings <ssec:string>`, using
whatever length that value currently holds. The shape-specific built-ins
keep the domains their own sections describe: ``rows`` and ``columns``
require a two-dimensional matrix, and ``format`` takes a scalar.

Applying a built-in outside its defined domain -- ``reverse``/``length`` on
a non-1-D value, ``rows``/``columns`` on a non-2-D value, or ``format`` on a
non-scalar -- is a compile-time error; the compiler must emit a
``TypeError`` (see :ref:`sec:errors`).

.. _ssec:builtIn_length:

Length
------

``length`` takes a single-dimensional array of any element type, and
returns an integer representing the number of elements in the array.
``length`` is not defined for an array of rank greater than 1; use ``rows``
and ``columns`` (see :ref:`ssec:builtIn_rows_cols`) for a two-dimensional
matrix instead.

::

         integer[*] v = 1..5;

         length(v) -> std_output; /* Prints 5 */

Because an array is :term:`initialization`-time sized, ``length`` applied to
an array is invariant after :term:`initialization`: every call returns the
same number. Applied to a :ref:`vector <ssec:vector>` (or a
:ref:`string <ssec:string>`), ``length`` returns the value's *current*
length instead, so two calls may return different numbers if the vector grew
in between. In this role ``length`` is simply the built-in spelling of the
vector's :ref:`len <sssec:vec_methods>` method.

::

         var vector<integer> v = [1, 2, 3];

         length(v) -> std_output; /* Prints 3 */

         call v.push(4);          /* 'v' is now [1, 2, 3, 4] */

         length(v) -> std_output; /* Prints 4 */


.. _ssec:builtIn_rows_cols:

Rows and Columns
----------------

The built-ins ``rows`` and ``columns`` report the dimensions of a
two-dimensional array (a :ref:`matrix <ssec:matrix>`): ``rows`` returns the
number of rows and ``columns`` the number of columns. (There is no
rank-agnostic ``shape`` built-in in this version of the language.)

::

         integer[*][*] M = [[1, 2, 3], [4, 5, 6]];

         rows(M) -> std_output;    /* Prints 2 */
         columns(M) -> std_output; /* Prints 3 */

.. _ssec:builtIn_reverse:

Reverse
-------

The reverse built-in takes any single-dimensional array, vector, or string, and
returns a reversed *array*. Even when the argument is a vector or string, the
result is an array value -- vector-ness (string-ness) is not preserved, just as
for the element-wise operators (see :ref:`sssec:vec_ops`). The resulting array
may of course be implicitly cast back to a vector or string when stored into
one.

::

         integer[*] v = 1..5;
         integer[*] w = reverse(v);

         v -> std_output; /* Prints [1, 2, 3, 4, 5] */
         w -> std_output; /* Prints [5, 4, 3, 2, 1] */

.. _ssec:builtIn_format:

Format
-------

The ``format`` built-in takes any :term:`scalar <scalar type>` as input and
returns a ``string`` containing the formatted value of the scalar. The result
uses the same representation the scalar's type has when sent to an output
stream (see :ref:`sssec:output_format`); a type with no defined output format
(a ``tuple`` or ``struct``) cannot be formatted.

::

         integer i = 24;
         real r = 2.4;

         "i = " || format(i) || ", r = " || format(r) || '\n' -> std_output;
         // Prints: "i = 24, r = 2.4\n"

Note that ``format`` allocates space to hold the return string; the
implementation is responsible for reclaiming it.

.. _ssec:builtIn_stream_state:

Stream State
------------

When reading values of certain types from ``std_input`` it is possible that an
error is encountered, or that the end of the stream has been encountered. In
order to handle these situations *Gazprea* provides a built-in procedure that is
implicitly defined in every file:

::

  procedure stream_state(var input_stream) returns integer;

The signature is notional: ``input_stream`` is not a *Gazprea* type, and
the only valid argument is ``std_input``. The form is general enough that
it could be reused if the language were expanded to include multiple input
streams.

The returned state codes, the initial state, and the per-type behavior of
reads are specified in :ref:`sssec:stream_error`. In brief: ``0`` means the
last read succeeded, ``1`` that it encountered an error, and ``2`` that it
encountered the end of the stream.

::

    var boolean b;
    var integer i;

    // Input stream: 9
    b <- std_input;              // b = false (error reading boolean)
    i = stream_state(std_input); // i = 1     (last read was error)
    i <- std_input;              // i = 9     (successfully read integer)
    i = stream_state(std_input); // i = 0     (last read was success)
    b <- std_input;              // b = false (read end of stream)
    i = stream_state(std_input); // i = 2     (last read was end of stream)


The input stream is described in more detail in the
:ref:`input stream <ssec:input>` section.
