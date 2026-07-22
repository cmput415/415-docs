.. _sec:builtIn:

Built-In Functions
==================

*Gazprea* has some built-in functions. These built in functions may have
some special behaviour that normal functions can not have, for instance
many of them will work on arrays of any element type.
Normally a function must specify the element type of an array argument.

The name of built in functions are reserved and a user program cannot
define a function or a procedure with the same name as a built-in function.
If a :term:`declaration` or a :term:`definition` with the same name as a
built-in function is encountered in a *Gazprea* program, then the compiler
must issue a ``SymbolError`` (see :ref:`sec:errors`).

Note that although the examples below all use arrays, all the built-ins work
on Vectors and Strings, since they are always compatible with arrays.

.. _ssec:builtIn_length:

Length
------

``length`` takes an array of any element type, and returns an integer
representing the number of elements in the array.

::

         integer[*] v = 1..5;

         length(v) -> std_output; /* Prints 5 */


.. _ssec:builtIn_rows_cols:

Shape
-----

The built-in ``shape`` operates on arrays of any dimension, and returns an
array listing the size of each dimension.

::

         integer[*][*] M = [[1, 2, 3], [4, 5, 6]];

         shape(M) -> std_output; /* Prints [2, 3] */

.. _ssec:builtIn_reverse:

Reverse
-------

The reverse built-in takes any single dimensional array, Vector, or String, and returns a
reversed version of it.

::

         integer[*] v = 1..5;
         integer[*] w = reverse(v);

         v -> std_output; /* Prints [1, 2, 3, 4, 5] */
         w -> std_output; /* Prints [5, 4, 3, 2, 1] */

.. _ssec:builtIn_format:

Format
-------

The ``format`` built-in takes any :term:`scalar <scalar type>` as input and
returns a ``string`` containing the formatted value of the scalar.

::

         integer i = 24;
         real r = 2.4;

         "i = " || format(i) || ", r = " || format(r) || '\n' -> std_output;
         // Prints: "i = 24, r = 2.4\n"

Note that ``format`` will have to allocate space to hold the return string.
You will have to figure out how to manage the memory so it is reclaimed
eventually.

.. _ssec:builtIn_stream_state:

Stream State
------------

When reading values of certain types from ``std_input`` it is possible that an
error is encountered, or that the end of the stream has been encountered. In
order to handle these situations *Gazprea* provides a built in procedure that is
implicitly defined in every file:

::

  procedure stream_state(var input_stream) returns integer;

The signature is notional: ``input_stream`` is not a *Gazprea* type, and
the only valid argument is ``std_input``. The form is general enough that
it could be reused if the language were expanded to include multiple input
streams.

The returned state codes, the initial state, and the per-type behaviour of
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
