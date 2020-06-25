.. _sec:builtIn:

Built In Functions
==================

*Gazprea* has some built in functions. These built in functions may have
some special behaviour that normal functions can not have, for instance
many of them will work on vectors of any base type. Normally a function
must specify the base type of a vector specified.

The name of built in functions are reserved and a user program cannot
define a function or a procedure with the same name as a built in
function. If a declaration or a definition with the same name as a
built-in function is encountered in a *Gazprea* program, then the
compiler should issue an error message.

.. _sec:length:

Length
------

``length`` takes a vector of any base type, and returns an integer
representing the length of the vector.

::

         integer vector v = 1..5;

         length(v) -> out; /* Prints 5 */

.. _sec:rowsColumns:

Rows and Columns
----------------

The built-ins ``rows`` and ``columns`` operate on matrices of any
dimension and type. ``rows`` returns the number of rows in a matrix, and
``columns`` returns the number of columns in the matrix.

::

         integer matrix M = [[1, 2, 3], [4, 5, 6]];

         rows(M) -> out; /* Prints 2 */
         columns(M) -> out; /* Prints 3 */

.. _sec:reverse:

Reverse
-------

The reverse built-in takes any vector, and returns a reversed version of
the vector.

::

         integer vector v = 1..5;
         integer vector w = reverse(v);

         v -> out; /* Prints 12345 */
         w -> out; /* Prints 54321 */

.. _sec:streamState:

Stream State
------------

When reading in values from stdin of certain types it is possible that
an error is encountered, or that the end of the stream has been
encountered. In order to handle these situations the language provides a
built in function:

::

         stream_state(inp)

This function can only be called with the input stream as a parameter,
but it’s general enough that it could be used if the language were
expanded to include multiple input streams.

When called ``stream_state`` will return an integer value. The return
value is an error code defined as follows:

-  0: Last read from the stream was successful

-  1: Last read from the stream encountered an error.

-  2: Last read from the stream encountered the end of the stream.

When an error is encountered the value assigned to the variable used in
the stream read operation is ``null``. When an end of stream is
encountered ``null`` is assigned to variables of all types except for
character. In this case character is assigned the ASCII EOF value.

When a read from the stream is not successful, and ``stream_state``
returns non-0, then the stream must be rewound to where it was before
the read started.

Reading a character never causes an error. The character will either be
successfully read, or the end of the stream has been reached and
character is assigned EOF for each subsequent read.

When reading anything else if something is read which does not match the
data type (for instance if the letter ’a’ is read while trying to parse
an integer), then this is an error. In this case the value returned by
the stream is ``null``, and ``stream_state`` should return 1. Or, if
only whitespace and the end of the stream is encountered the stream is
rewound to where it was before the read, ``null`` is returned, and
``stream_state`` will return 2.
