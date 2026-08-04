Statements
----------

Our version of LOLCODE supports seven types of statements:

-  :ref:`sssec:declaration`
-  :ref:`sssec:assignment`
-  :ref:`sssec:cast`
-  :ref:`sssec:io`
-  :ref:`sssec:loop`
-  :ref:`sssec:conditional`
-  :ref:`sssec:case`

.. _sssec:io:

Input/Output
~~~~~~~~~~~~

The print (to STDOUT or the terminal) operator is ``VISIBLE``. It has infinite arity and implicitly concatenates all of its arguments after casting them to YARNs. It is terminated by the statement delimiter (line end, comma, or single line comment). The output is automatically terminated with a carriage return, unless the final token is terminated with an exclamation point (``!``), in which case the carriage return is suppressed.

::

VISIBLE <expression> [<expression> ...][!]

To accept input from the user, the keyword is

::

GIMMEH <variable>


which takes ``YARN`` for input and stores the value in the given variable.

.. _sssec:loop:

Loop
~~~~

Simple loops are demarcated with ``IM IN YR <label>`` and ``IM OUTTA YR <label>``.
Loops defined this way are infinite loops that must be explicitly exited with a GTFO break. Currently, the ``<label>`` is required, but is unused, except for marking the start and end of the loop.

The full version of the language includes iterated loops, but you are not
required to implement them for this assignment.

.. _sssec:conditional:

If-then
~~~~~~~

An **If** statement begins with a comparison:

::

   BOTH SAEM <x> [AN] <y>   BTW WIN iff x == y
   DIFFRINT <x> [AN] <y>    BTW WIN iff x != y


Comparisons are performed as integer math in the presence of two ``NUMBR`` s,
or string comparisons if both expressions are ``YARN`` s. Otherwise, there is
no automatic casting in the equality, so ``BOTH SAEM "3" AN 3`` is ``FAIL``.

There are no special numerical comparison operators. Greater-than and similar comparisons are done idiomatically using the minimum and maximum operators:

::

    BOTH SAEM <x> AN BIGGR OF <x> AN <y>   BTW x >= y
    BOTH SAEM <x> AN SMALLR OF <x> AN <y>  BTW x <= y
    DIFFRINT <x> AN SMALLR OF <x> AN <y>   BTW x < y
    DIFFRINT <x> AN BIGGR OF <x> AN <y>    BTW x > y

In the base form, the if/then construct uses four keywords: ``O RLY?``, ``YA RLY``, ``NO WAI``, and ``OIC``.

``O RLY?`` branches to the block begun with ``YA RLY`` if the comparison is ``WIN``, and branches to the ``NO WAI`` block if the comparison is ``FAIL``.
The code block introduced with ``YA RLY`` is implicitly closed when ``NO WAI`` is reached. The ``NO WAI`` block is closed with ``OIC``. Of course, the *else*
is optional, so ``OIC`` may also close a ``YA RLY`` block.
The general form is then as follows:

::

   <comparison>
   O RLY?
      YA RLY
        <code block>
      [NO WAI
        <code block>]
   OIC

while an example showing the ability to put multiple statements on a line separated by a comma would be:

::

    BOTH SAEM ANIMAL AN "CAT", O RLY?
      YA RLY, VISIBLE "J00 HAV A CAT"
      NO WAI, VISIBLE "J00 SUX"
    OIC


The **Elseif** construction adds a little bit of complexity.
Optional ``MEBBE <comparison>`` blocks may appear between the ``YA RLY`` and ``NO WAI`` (``OIC``) blocks.
If the ``<comparison>`` following ``MEBBE`` is ``WIN``, then that block is
executed; if not, the block is skipped until the following ``MEBBE``, ``NO WAI``, or ``OIC``. The full expression syntax is then as follows:

::
   
    <expression>
    O RLY?
      YA RLY
        <code block>
     [MEBBE <expression>
        <code block>
     [MEBBE <expression>
        <code block>
      ...]]
     [NO WAI
        <code block>]
   OIC


An example of this conditional is then:

::

  BOTH SAEM ANIMAL AN "CAT"
    O RLY?
      YA RLY, VISIBLE "J00 HAV A CAT"
      MEBBE BOTH SAEM ANIMAL AN "MAUS"
        VISIBLE "NOM NOM NOM. I EATED IT."
  OIC

.. _sssec:case:

Case
~~~~


The LOLCODE keyword for switches is ``WTF?``. The ``WTF?`` operator is given an
``<expression>`` that is used as the value for comparison.
A comparison block is opened by ``OMG`` and must be a literal, not an expression.
Each ``OMG`` literal must be unique. The ``OMG`` block can be followed by any number of statements and may be terminated by a ``GTFO``, which breaks to the end of the the ``WTF`` statement. If an ``OMG`` block is not terminated by a ``GTFO``, then the next ``OMG`` block is executed as is the next until a ``GTFO`` or the end of the ``WTF`` block is reached. The optional default case, if none of the literal comparisons is ``WIN``, is signified by ``OMGWTF``.

::

     <expression>, WTF?
      OMG <value literal>
        <code block>
     [OMG <value literal>
        <code block> ...]
     [OMGWTF
        <code block>]
    OIC

::
   
    COLOR, WTF?
      OMG "R"
        VISIBLE "RED FISH"
        GTFO
      OMG "Y"
        VISIBLE "YELLOW FISH"
      OMG "G"
      OMG "B"
        VISIBLE "FISH HAS A FLAVOR"
        GTFO
      OMGWTF
         VISIBLE "FISH IS TRANSPARENT"
    OIC

In this example, the output results of evaluating the variable ``COLOR`` would be:

"R":

::
   
    RED FISH

"Y":

::

    YELLOW FISH
    FISH HAS A FLAVOR

"G":

::

    FISH HAS A FLAVOR

"B":

::

    FISH HAS A FLAVOR

none of the above:

::

    FISH IS TRANSPARENT
  



