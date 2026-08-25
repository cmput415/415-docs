.. _sec:streams:

Streams
=======

*Gazprea* has two streams: ``std_output`` and ``std_input``,
which are used for writing to `stdout` and reading from `stdin` respectively.


.. _ssec:output:

Output Stream
-------------

Output streams use the following syntax:

::

     <exp> -> std_output;

.. _sssec:output_format:

Output Format
~~~~~~~~~~~~~

Values of the following :term:`primitive types <primitive type>` are
treated as follows when sent to an output stream:

-  :ref:`ssec:character`: Prints the character.

-  :ref:`ssec:integer`: Converts it to a string representation, and then prints
   it.

-  :ref:`ssec:real`: Converts it to a string representation, and then prints it.
   This is the same behavior as the `%g specifier in
   printf <http://www.cplusplus.com/reference/cstdio/printf/>`__.

-  :ref:`ssec:boolean`: Prints T for true, and F for false.

:ref:`Arrays <ssec:array>` print their contents according to the rules above,
with square braces surrounding their elements and with spaces only *between*
values. For example:

::

     integer[*] v = 1..4;
     v -> std_output;

prints the following:

::

     [1 2 3]

:ref:`Vectors <ssec:vector>` print exactly as :ref:`arrays <ssec:array>`
do, using whatever length the vector holds at the time of the output
statement. A :ref:`string <ssec:string>` is the sole exception: although
a string is a vector of characters, it prints its characters contiguously
rather than in bracketed array form, as shown next.

:ref:`Strings <ssec:string>` print their contents as a contiguous sequence of
characters. For example:

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

No other type may be sent to a stream; the compiler must emit a ``TypeError``
(see :ref:`sec:errors`). For instance, a tuple or a struct cannot be sent to a
stream. A procedure call may not appear as a stream operand at all, since that
is not one of the :ref:`positions in which a procedure call may appear
<ssec:procedure_call_positions>`; the compiler must emit a ``CallError`` (see
:ref:`sec:errors`). Also, empty arrays and matrices can be sent to streams, but
not empty literals (e.g. ``[]``), because they have no type; sending one must
emit a ``TypeError`` (see :ref:`sec:errors`). A *typed* empty array prints as an
empty pair of brackets:

::

     integer[*] empty = [];
     empty -> std_output;

prints the following:

::

     []

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

     <lvalue> <- std_input;

An :term:`lvalue` may be anything that can appear on the left hand side of an
assignment statement (see :ref:`sec:expressions`) -- not only a plain variable
but also, for example, an array element:

::

     var integer[3] v = [0, 0, 0];
     v[2] <- std_input;   // reads a single integer into element 2 of v

The primitive-only restriction below still applies: the target must designate a
single primitive location.

Input streams may only work on the following primitive types:

-  ``character``: Reads a single character from stdin. Note that a
   character read never sets :ref:`error state <sssec:stream_error>` 1;
   reaching the end of the stream still sets state 2.

-  ``integer``: Reads an integer from stdin. If an integer could not be
   read, an :ref:`error state <sssec:stream_error>` is set on this stream.

-  ``real``: Reads a real from stdin. If a real could not be read, an
   :ref:`error state <sssec:stream_error>` is set on this stream.

-  ``boolean``: Reads a boolean from stdin. If a boolean value could not
   be read, an :ref:`error state <sssec:stream_error>` is set on this stream.

Implicit casting is not performed for stream input over any type.

.. _sssec:input_format:

Input Semantics
~~~~~~~~~~~~~~~

``std_input`` expects an input stream of values which do not need to be
whitespace separated. A read will consume the stream until a character or EOF
occurs that breaks the pattern match for the given type's specifier. The
longest successful match is returned.

In general input stream semantics are designed for parity with ``scanf``. The
only differences are the :ref:`ssec:builtIn_stream_state`, a boolean specifier
and a restriction on the maximum number of bytes that can be consumed in a
single read to 512.

For each of the allowed types the semantics are given below.

Reading a ``character`` from stdin consumes the first byte that can be read
from the stream. If the end of the stream is encountered, the character read is
``0xFF`` (``255``) -- ``character`` values are :ref:`unsigned bytes <ssec:character>`
in ``0`` to ``255``, so there is no ``-1`` -- and the end-of-stream
:ref:`error state <sssec:stream_error>` is set. Because a legitimate ``0xFF``
byte is indistinguishable from end-of-stream by its value alone, a program must
consult :ref:`stream_state <ssec:builtIn_stream_state>` to tell the two apart;
this is the reason ``stream_state`` exists. There is no concept of skipping
whitespace for characters, since space and escaped characters must be readable.

An ``integer`` from stdin can take any legal format described in the
:ref:`integer literal <sssec:integer_lit>` section. It may also be preceded by
a single negative or positive sign. All preceding whitespace before the number
or sign character may be skipped up to the limit imposed by the 512 byte read
restriction.

A ``real`` input from stdin can take any legal format described in the
:ref:`real literal <sssec:real_lit>` section. It may be preceded by a single
negative or positive sign, and preceding whitespace may be skipped in the same
way as integers; the sign and the digits of the number itself, however, must be
contiguous -- no whitespace may appear *within* the value.

A ``boolean`` input from stdin is either ``T`` or ``F``. Preceding whitespace
may be skipped in the same way as integers and reals.

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

   F 1

(``1.`` reads as the real 1.0, which prints as ``1`` under the ``%g``
format rule above) because the white space is consumed for characters and
skipped for other types.


.. _sssec:stream_error:

Error Handling
~~~~~~~~~~~~~~

When reading ``boolean``, ``integer``, and ``real`` from stdin, it is
possible that the end of the stream or an error is encountered. In order to
handle these situations *Gazprea* provides a built-in procedure that is
implicitly defined in every file: ``stream_state`` (see
:ref:`ssec:builtIn_stream_state` for its signature). ``stream_state``
returns ``0`` if the last read succeeded, ``1`` if it encountered an
error, and ``2`` if it encountered the end of the stream. Before any read
has been issued it returns ``0``.

Reading a ``character`` can never set error state 1. The character will
either be successfully read, or the end of the stream will be reached: the
read then yields the ``character`` byte ``0xFF`` (``255``, i.e.
``as<character>(-1)``) and sets state 2.

When a read sets error state ``1`` -- which is possible only for ``boolean``,
``integer``, and ``real`` (a ``character`` read never sets state ``1``) -- the
:term:`zero value` for the type being read is assigned to the target, the
implicit ``stream_state`` is set to ``1``, and the input stream remains
pointing to the same position as before the read occurred. Reaching the end of
the stream (state ``2``) instead assigns the value from the Return column of the
table below -- the type's zero value for ``boolean``/``integer``/``real``, and
``0xFF`` (``255``, i.e. ``as<character>(-1)``) for a ``character`` -- and sets
``stream_state`` to ``2``.

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

This table summarizes an input stream's possible error states after a read of a
particular data type.

========= ============= ========= =================
Type      Situation     Return    ``stream_state``
========= ============= ========= =================
Boolean   error         ``false`` 1
\         end of stream ``false`` 2
Character error         N/A       N/A
\         end of stream ``0xFF``  2
Integer   error         ``0``     1
\         end of stream ``0``     2
Real      error         ``0.0``   1
\         end of stream ``0.0``   2
========= ============= ========= =================
