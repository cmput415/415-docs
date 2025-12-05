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

:ref:`Arrays <ssec:array>` print their contents according to the rules above, with square
braces surrounding its elements and with spaces only *between* values.
For example:

::

     integer[*] v = 1..3;
     v -> std_output;

prints the following:

::

     [1 2 3]

:ref:`strings <ssec:string>` print their contents as a contiguous sequence of characters.
For example:

::

     string str = "Hello, World!";
     str -> std_output;

prints the following:

::

     Hello, World!

:ref:`Matrices <ssec:matrix>` print like an array of arrays. For example:

::

     [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> std_output;

prints the following:

::

     [[1 2 3] [4 5 6] [7 8 9]]

No other type may be sent to a stream. For instance,
procedures with no return type and tuples cannot be sent to streams.
Also, empty arrays and matrices can be send to streams, but not empty
literals (e.g. ``[]``), because they have no type.

Note that there is **no automatic new line or spaces printed.** To print
a new line, a user must explicitly print the new line or space
character. For example:

::

     '\n' -> std_output;
     ' ' -> std_output;

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

Type promotion is not performed for stream input over any type.

   .. _sssec:input_format:

Input Semantics
~~~~~~~~~~~~~~~

``std_input`` expects an input stream of values which do not need to be
whitespace separated. A read will consume the stream until a character or
EOF occurs that breaks the pattern match for the given types specifier. The longest 
successful match is returned.

In general input stream semantics are designed for parity with ``scanf``.
The only differences are the :ref:`ssec:builtIn_stream_state`, a boolean specifier
and a restriction on the maximum number of bytes that can be consumed in a single read to 512.

For each of the allowed types the semantics are given below. 

Reading a ``character`` from stdin consumes the first byte that can be read from the
stream. If the end of the stream is encountered, then a value of ``-1`` is set. There
is no concept of skipping whitespace for characters, since space and escaped characters
must be readable.

An ``integer`` from stdin can take any legal format described in the
:ref:`integer literal <sssec:integer_lit>` section. It may also be preceded by
a single negative or positive sign. All preceeding whitespace before the number or
sign character may be skipped up to the limit imposed by the 512 byte read restriction.

A ``real`` input from stdin can take any legal format described in the
:ref:`real literal <sssec:real_lit>` section with the exception that no
whitespace may be present. It may also be proceeded by a single negative or
positive sign. Preceeding whitespace may be skipped in the same way as integers. 

A ``boolean`` input from stdin is either ``T`` or ``F``. Preceeding whitespace may be
skipped in the same way as integers and reals. 

For the following program:

::

   var boolean b;
   var character c;
   var integer i;
   var real r;
   b <- std_input;
   i <- std_input;
   c <- std_input;
   r <- std_input;
   format(b) || " " || format(r) -> std_output;

And this input (where '\\t' is TAB, '*' is space, and each line ends with a
newline ('\\n'):

::

   \tF\n
   1\n
   *1.\n

The output would be:

::

   F 1.0

because the white space is consumed for characters and skipped for other types.


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

When an error occurs the the null value is assigned and the input stream
remains pointing to the same position as before the read occured.

The program below demonstrates 4 reads which set the error
states 1,0,0,2 respectively.

::

    var integer ss;
    var integer i;
    var boolean b;
    var character c;

    i <- std_input;
    i -> std_output;
    ss = stream_state(std_input);
    ss -> std_output;

    c <- std_input; //eat the .
   
    i <- std_input;
    i -> std_output;
  
    c <- std_input;
    ss = stream_state(std_input);
    ss -> std_output;
    
With the input stream: 

::

  .7

And the expected output:

::

  0172

This table summarizes an input stream’s possible error states after a read of a
particular data type.

========= ============= ========= =================
Type      Situation     Return    ``stream_state``
========= ============= ========= =================
Boolean   error         ``false`` 1
\         end of stream ``false`` 2
Character error         N/A       N/A
\         end of stream ``-1``    2
Integer   error         ``0``     1
\         end of stream ``0``     2
Real      error         ``0.0``   1
\         end of stream ``0.0``   2
========= ============= ========= =================
