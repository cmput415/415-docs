.. _sec:builtIn:

Built-in Functions, Procedures and Methods
===========================================

*Gazprea* has some built-in functions and procedures
that do not follow the usual
rules for functions and procedures.

The names of the built-in functions and procedures are reserved. A user program
may not declare *any* function or procedure identifier
with the same name as a built-in function or procedure; doing
so would shadow the built-in, and the compiler must emit a ``SymbolError``
(see :ref:`sec:errors`). These names are reserved semantically rather than being
syntactic :ref:`keywords <sec:keywords>`.

The :ref:`vector/string method <sssec:vec_methods>` names (``push``,
``append``, ``len``), by contrast, are **not** reserved. They live in a method
namespace associated with the compiler-defined ``vector`` object
and so do not collide with the
global identifier namespace. A user may freely declare, say, a ``function
len()`` or a variable named ``push``.

Note that although the examples below all use arrays, the array-shaped
built-ins (``length``, ``reverse``) also work on
:ref:`vectors <ssec:vector>` and :ref:`strings <ssec:string>`, using
whatever length that value currently holds. The shape-specific built-ins
keep the domains their own sections describe: ``rows`` and ``columns``
require a two-dimensional matrix, and ``format`` takes only scalars.

Applying a built-in outside its defined domain 
is a compile-time error and the compiler must emit a
``TypeError`` (see :ref:`sec:errors`).

.. _ssec:builtIn_signatures:

Signatures
----------

*Gazprea* has no user-facing type parameters (they may be added in a future
revision), but the built-ins are generic over element and scalar types. Their
signatures are therefore written below with a ``[T]`` type-parameter notation
purely for exposition: ``function id[T](T obj) returns T;`` reads as "``id`` is
generic over ``T``". This notation is **not** part of the language.

::

    function length[T](T[*] arr) returns integer;    // also accepts a vector<T> / string
    function rows[T](T[*][*] mat) returns integer;
    function columns[T](T[*][*] mat) returns integer;
    function reverse[T](T[*] arr) returns T[*];       // also accepts a vector<T> / string
    function format[T](T value) returns string;       // T is a scalar type
    procedure stream_state(var input_stream) returns integer; // notional; see below

The per-built-in sections below give each domain and its error conditions in
full.

.. _ssec:builtIn_methods:

Vector and String Methods
-------------------------

In addition to these free-standing built-ins, ``vector`` and ``string`` values
carry **methods** -- ``push``, ``append``, and ``len`` -- invoked with receiver
syntax (``v.len()``). These are specified with the type, in
:ref:`sssec:vec_methods`, not here. In particular, ``len`` (a method, on vectors
and strings only) and ``length`` (a built-in, accepting arrays, vectors, and
strings) answer the same question with different spellings and different domains:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Query on ``x``
     - ``length(x)`` (built-in)
     - ``x.len()`` (method)
   * - array ``T[n]``
     - the fixed length ``n``
     - ``TypeError`` -- arrays have no methods
   * - ``vector<T>`` / ``string``
     - the current length
     - the current length

.. _ssec:builtIn_length:

Length
------

``length`` takes an rank-1 array of any element type, and
returns an integer representing the number of elements in the array.
``length`` is not defined for an array of rank greater than 1; use ``rows``
and ``columns`` (see :ref:`ssec:builtIn_rows_cols`) for a two-dimensional
matrix instead. In future editions of the spec this may be extended to a
generic ``shape`` function, but that is left to future revisions of the
course.

.. gazprea-example-wrap::
   :name: builtin_length

   integer[*] v = 1..5;
   length(v) -> std_output; /* Prints 5 */

   --- output ---
   5

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
rank-2 array (a :ref:`matrix <ssec:matrix>`): ``rows`` returns the
number of rows and ``columns`` the number of columns.

.. gazprea-example-wrap::
   :name: builtin_rows_columns

   integer[*][*] M = [[1, 2, 3], [4, 5, 6]];
   rows(M) -> std_output;    /* Prints 2 */
   '\n' -> std_output;
   columns(M) -> std_output; /* Prints 3 */

   --- output ---
   2
   3

.. _ssec:builtIn_reverse:

Reverse
-------

The reverse built-in takes any rank-1 array, vector, or string, and
returns a reversed *array*. Even when the argument is a vector or string, the
result is an array value. Vector-ness (string-ness) is not preserved, just as
for the element-wise operators (see :ref:`sssec:vec_ops`). The resulting array
may of course be implicitly cast back to a vector or string when stored into
one.

.. gazprea-example-wrap::
   :name: builtin_reverse

   integer[*] v = 1..5;
   integer[*] w = reverse(v);
   v -> std_output; /* Prints [1 2 3 4 5] */
   '\n' -> std_output;
   w -> std_output; /* Prints [5 4 3 2 1] */

   --- output ---
   [1 2 3 4 5]
   [5 4 3 2 1]

.. _ssec:builtIn_format:

Format
-------

The ``format`` built-in takes any :term:`scalar <scalar type>` as input and
returns a ``string`` containing the formatted value of the scalar. The result
uses the same representation the scalar's type has when sent to an output
stream (see :ref:`sssec:output_format`). This function only takes scalars;
a type with no defined output format
(a ``tuple`` or ``struct``) cannot be formatted.

.. gazprea-example-wrap::
   :name: builtin_format

   integer i = 24;
   real r = 2.4;
   "i = " || format(i) || ", r = " || format(r) || "\n" -> std_output;
   // Prints: "i = 24, r = 2.4\n"

   --- output ---
   i = 24, r = 2.4

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

.. gazprea-example-wrap::
   :name: builtin_stream_state
   :input: 9

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
