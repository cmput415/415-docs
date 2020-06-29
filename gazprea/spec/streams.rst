.. _sec:streams:

Streams
=======

Streams are an implicit language type only usable when a stream is
assigned to a variable declared ``var``. An input stream and an output
stream are *different types*. Both types have no valid conversions to
any other type nor any valid operations besides the stream in and out
operators.

*Gazprea* has two streams: stdout and stdin. As noted above they must be
assigned to a var They are not automatically available and cannot be
used in expressions other than as the right-hand-side of an assignment
statement. Therefore, streams *must be* assigned to a ``var`` as so:

::

     var out = std_output();
     var inp = std_input();

Streams cannot be duplicated, therefore, once a stream has been
assigned, it *cannot* be assigned to a new variable.

Streams cannot be ``const`` because the only operator defined on them
mutates the stream’s internal state. This means that a variable
initialised with a stream can be assigned a new stream of the same type.
This would create a new stream with a clean state. For example:

::

     var in = std_input();
     in = std_input();

Assigning a stream of a different type is a **type error**. For example,
this should result in an error.

::

     var in = std_input();
     in = std_output();

.. _ssec:output:

Output Stream
-------------

Output streams use the following syntax:

::

     <exp> -> out;

.. _sssec:output_format:

Output Format
~~~~~~~~~~~~~

Values of the following base types are treated as follows when sent to
an output stream:

-  ``character``: The character is printed.

-  ``integer``: Converted to a string representation, and then printed.

-  ``real``: Converted to a string representation, and then printed.
   This is the same behaviour as the `%g specifier in
   printf <http://www.cplusplus.com/reference/cstdio/printf/>`__.

-  ``boolean``: Print T for true, and F for false.

Vectors print their contents according to the rules above, with square
braces surrounding its elements and with spaces only *between* values.
For example:

::

     integer[*] v = 1..3;
     v -> out;

prints the following:

::

     [1 2 3]

Matrices print like a vector of vectors. For example:

::

     [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> out;

prints the following:

::

     [[1 2 3] [4 5 6] [7 8 9]]

No other type may be sent to a stream. For instance functions,
procedures, and tuples cannot be sent to streams.

Note that there is **no automatic new line or spaces printed.** To print
a new line, a user must explicitly print the new line or space
character. For example:

::

     '\n' -> out;
     ' ' -> out;

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

     <l-value> <- inp;

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

A ``character`` from stdin is the first byte that can be read from the
stream. If the end of the stream is encountered, then ``-1`` is
returned.

An ``integer`` from stdin can take any legal format described in the :ref:`integer literal <sssec:integer_lit>`
section. It may also be proceeded by a single negative or positive sign.

A ``real`` input from stdin can take any legal format described in the :ref:`real literal <sssec:real_lit>`
section. It may also be proceeded by a single negative or positive sign.

A ``boolean`` input from stdin is either ``T`` or ``F``.

Whitespace will separate values in stdin, but take note that a
whitespace character *can* also be read from stdin and assigned to a
character variable.

When reading a value, if any other input were to be in the stream during
the read then an is set. For example, the following program:

::

     boolean b;
     var stdin = std_input();
     b <- stdin;

With the standard input stream containing this:

::

   Ta

An :ref:`error state <sssec:stream_error>` would be set on the stream.

.. _sssec:stream_error:

Error Handling
~~~~~~~~~~~~~~

When reading ``boolean``\ s, ``integer``\ s, and ``real``\ s from stdin, it is
possible that the end of the stream or an error is encountered. In order
to handle these situations *Gazprea* provides a built in procedure that
is implicitly defined in every file:

::

     procedure stream_state(var input_stream) returns integer;

This function can only be called with an input stream as a parameter.
When called, ``stream_state`` will return an integer valued error code
defined as follows:

-  ``0``: Last read from the stream was successful.

-  ``1``: Last read from the stream encountered an error.

-  ``2``: Last read from the stream encountered the end of the stream.

When an error or end of stream is encountered the value returned is the
type-appropriate ``null``.

Reading a character can never cause an error. The character will either
be successfully read or the end of the stream will be reached and ``-1``
will be returned on this and subsequent reads.

This table summarizes an input stream’s possible error states after a
read of a particular data type.

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
