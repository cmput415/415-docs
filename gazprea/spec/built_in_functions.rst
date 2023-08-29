.. _sec:builtIn:

Built In Functions
==================

*Gazprea* has some built in functions. These built in functions may have
some special behaviour that normal functions can not have, for instance
many of them will work on vectors of any element type. Normally a function
must specify the element type of a vector specified.

The name of built in functions are reserved and a user program cannot
define a function or a procedure with the same name as a built in
function. If a declaration or a definition with the same name as a
built-in function is encountered in a *Gazprea* program, then the
compiler should issue an error message.

.. _ssec:builtIn_length:

Length
------

``length`` takes a vector of any element type, and returns an integer
representing the length of the vector.

::

         integer[*] v = 1..5;

         length(v) -> std_output; /* Prints 5 */

.. _ssec:builtIn_rows_cols:

Rows and Columns
----------------

The built-ins ``rows`` and ``columns`` operate on matrices of any
dimension and type. ``rows`` returns the number of rows in a matrix, and
``columns`` returns the number of columns in the matrix.

::

         integer[*, *] M = [[1, 2, 3], [4, 5, 6]];

         rows(M) -> std_output; /* Prints 2 */
         columns(M) -> std_output; /* Prints 3 */

.. _ssec:builtIn_reverse:

Reverse
-------

The reverse built-in takes any vector, and returns a reversed version of
the vector.

::

         integer[*] v = 1..5;
         integer[*] w = reverse(v);

         v -> std_output; /* Prints 12345 */
         w -> std_output; /* Prints 54321 */

.. _ssec:builtIn_format:

Format
-------

The ``format`` built-in takes any scalar as input and returns a string
containing the formatted value of the scalar.

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

This function can only be called with the ``std_input`` as a parameter, but it’s
general enough that it could be used if the language were expanded to include
multiple input streams.

When called, ``stream_state`` will return an integer value. The return value is
an error code defined as follows:

  - ``0``: Last read from the stream was successful
  - ``1``: Last read from the stream encountered an error.
  - ``2``: Last read from the stream encountered the end of the stream.

::

         boolean b;
         integer i;

         input: 9 10
         b <- std_input // 9
         x = stream_state(std_input) // 1 - Wrong Input Type
         i <- std_input // 9
         x = stream_state(std_input) // 0 - Success
         i <- std_input // 10
         x = stream_state(std_input) // 2 - No More Input
