.. _sec:streams:

Streams
=======

*Gazprea* has two streams: ``std_output`` and ``std_input``,
which are used for writting to `stdout` and reading from `stdin` respectively.


.. _ssec:output:

Output Stream
-------------

Output streams use the following syntax:

::

     <exp> -> std_output;

.. _sssec:output_format:

Output Format
~~~~~~~~~~~~~

Values of the following base types are treated as follows when sent to
an output stream:

-  :ref:`ssec:character`: The character is printed.

-  :ref:`ssec:integer`: Converted to a string representation, and then printed.

-  :ref:`ssec:real`: Converted to a string representation, and then printed.
   This is the same behaviour as the `%g specifier in
   printf <http://www.cplusplus.com/reference/cstdio/printf/>`__.

-  :ref:`ssec:boolean`: Prints T for true, and F for false.

:ref:`Vectors <ssec:vector>` print their contents according to the rules above, with square
braces surrounding its elements and with spaces only *between* values.
For example:

::

     integer[*] v = 1..3;
     v -> std_output;

prints the following:

::

     [1 2 3]

:ref:`Strings <ssec:string>` print their contents as a contiguous sequence of characters.
For example:

::

     string str = "Hello, World!";
     str -> std_output;

prints the following:

::

     Hello, World!

:ref:`Matrices <ssec:matrix>` print like a vector of vectors. For example:

::

     [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> std_output;

prints the following:

::

     [[1 2 3] [4 5 6] [7 8 9]]

No other type may be sent to a stream. For instance functions,
procedures, and tuples cannot be sent to streams.

Note that there is **no automatic new line or spaces printed.** To print
a new line, a user must explicitly print the new line or space
character. For example:

::

     '\n' -> std_output;
     ' ' -> std_output;

.. _sssec:stream_nai:

Null and Identity
~~~~~~~~~~~~~~~~~

If ``null`` or ``identity`` is sent to a stream then the result is a
null or identity character being printed.

.. _ssec:input:

Input Stream
------------

Input streams use the following syntax:

::

     <l-value> <- std_input;

An l-value may be anything that can appear on the left hand side of an
assignment statement. Consider reading the discussion of an l-value
`here <https://en.wikipedia.org/wiki/Value_(computer_science)#Assignment:_l-values_and_r-values>`__.

Input streams may only work on the following base types:

-  ``character``: Reads a single character from stdin. Note that there
   can be no :ref:`error state <sssec:stream_error>` for reading characters.

-  ``integer``: Reads an integer from stdin. If an integer could not be
   read, an :ref:`error state <sssec:stream_error>` is set on this stream.

-  ``real``: Reads a real from stdin. If a real could not be read, an :ref:`error state <sssec:stream_error>` is
   set on this stream.

-  ``boolean``: Reads a boolean from stdin. If a boolean value could not
   be read, an :ref:`error state <sssec:stream_error>` is set on this stream.

.. _sssec:input_format:

Input Format
~~~~~~~~~~~~

Whitespace will separate values in stdin, but take note that a whitespace
character *can* also be read from stdin and assigned to a character variable.

A ``character`` from stdin is the first byte that can be read from the stream.
If the end of the stream is encountered, then ``-1`` is returned.

An ``integer`` from stdin can take any legal format described in the
:ref:`integer literal <sssec:integer_lit>` section. It may also be proceeded by
a single negative or positive sign.

A ``real`` input from stdin can take any legal format described in the
:ref:`real literal <sssec:real_lit>` section with the exception that no
whitespace may be present. It may also be proceeded by a single negative or
positive sign.

A ``boolean`` input from stdin is either ``T`` or ``F``.

When reading a value, if any other input were to be in the stream during the
read then an :ref:`error state <sssec:stream_error>` is set. For example, the
following program:

::

  boolean b;
  b <- std_input;

With the standard input stream containing this:

::

   Ta

An :ref:`error state <sssec:stream_error>` would be set on the stream.

Type promotion is not performed for stream input.

.. _sssec:stream_error:

Error Handling
~~~~~~~~~~~~~~

When reading ``boolean``, ``integer``, and ``real`` from stdin, it is
possible that the end of the stream or an error is encountered. In order to
handle these situations *Gazprea* provides a built in procedure that is
implicitly defined in every file: ``stream_state`` (see
:ref:`ssec:builtIn_stream_state`).

Reading a ``character`` can never cause an error. The character will either be
successfully read or the end of the stream will be reached and ``-1`` will be
returned on this read.

Otherwise, when an error or the end of the stream is encountered, the value
returned is the type-appropriate ``null``.

Only when an error is encountered, the stream must be rewound to where it was
when the read started. This rewind includes any whitespace that may have been
skipped to in order to encounter the next token. This is because the subsequent
read may be for a ``character`` which should successfully read the rewound
whitespace. For example, with this program:

::

  integer i;
  character c;
  i <- std_input;
  i <- std_input;
  c <- std_input;

  i -> std_output;
  c -> std_output;
  '$' -> std_output;

and the input stream (with ``*`` representing ``' '``):

::

  5****10a

the output should be:

::

  0 $

and the remaining input stream should be:

::

  ***10a

Because this means you may have to skip a potentially nearly-infinite amount of
whitespace this specification, this specification limits the size of the "rewind
buffer" to 1024 characters. Therefore, no read from ``std_input`` will require
more than 1KB of characters from the current stream position to the end of the
next token. This means that you will only ever need to maintain at most 1024
characters in a buffer (1025 if a ``'\0'`` character is required). If more
characters than that are required to be read then the runtime should emit an
error.

This table summarizes an input stream’s possible error states after a read of a
particular data type.

========= ============= ========= =================
Type      Situation     Return    ``stream_state``
========= ============= ========= =================
Boolean   error         ``false`` 1
\         end of stream ``false`` 2
Character error         N/A       N/A
\         end of stream ``-1``    0
Integer   error         ``0``     1
\         end of stream ``0``     2
Real      error         ``0.0``   1
\         end of stream ``0.0``   2
========= ============= ========= =================
