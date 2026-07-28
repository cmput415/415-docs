Statements
----------

Our version of LOLCODE supports seven types of statements:

-  :ref:`sssec:declaration`
-  :ref:`sssec:assignment`
-  :ref:`sssec:cast`
-  :ref:`sssec:conditional`
-  :ref:`sssec:loop`
-  :ref:`sssec:case`
-  :ref:`sssec:io`

.. _sssec:conditional:

If-then
~~~~~~~

A bare expression statement (one not assigned to a variable) stores its result in the implicit variable ``IT``. ``IT`` holds that value until the next bare expression replaces it, and is what ``O RLY?`` and ``WTF?`` test against.

An if statement begins with a comparison:

Comparison is (currently) done with two binary equality operators:

::

   BOTH SAEM <x> [AN] <y>   BTW WIN iff x == y
   DIFFRINT <x> [AN] <y>    BTW WIN iff x != y


Comparisons are performed as integer math in the presence of two NUMBRs,
or string comparisons if both expressions are YARNs.
Otherwise, there is no automatic casting in the equality, so ``BOTH SAEM "3" AN 3`` is FAIL.

There are no special numerical comparison operators. Greater-than and similar comparisons are done idiomatically using the minimum and maximum operators.

::

    BOTH SAEM <x> AN BIGGR OF <x> AN <y>   BTW x >= y
    BOTH SAEM <x> AN SMALLR OF <x> AN <y>  BTW x <= y
    DIFFRINT <x> AN SMALLR OF <x> AN <y>   BTW x > y
    DIFFRINT <x> AN BIGGR OF <x> AN <y>    BTW x < y

In the base form, the if/then construct uses  four keywords: ``O RLY?``, ``YA RLY``, ``NO WAI``, and ``OIC``.

``O RLY?`` branches to the block begun with ``YA RLY`` if ``IT`` can be cast to WIN, and branches to the ``NO WAI`` block if ``IT`` is FAIL. The code block introduced with ``YA RLY`` is implicitly closed when ``NO WAI`` is reached. The ``NO WAI`` block is closed with ``OIC``. The general form is then as follows:

::

   <expression>
   O RLY?
      YA RLY
        <code block>
      NO WAI
        <code block>
   OIC

while an example showing the ability to put multiple statements on a line separated by a comma would be:

::

    BOTH SAEM ANIMAL AN "CAT", O RLY?
      YA RLY, VISIBLE "J00 HAV A CAT"
      NO WAI, VISIBLE "J00 SUX"
    OIC


The elseif construction adds a little bit of complexity. Optional ``MEBBE <expression>`` blocks may appear between the YA RLY and NO WAI blocks. If the ``<expression>`` following ``MEBBE`` is WIN, then that block is performed; if not, the block is skipped until the following ``MEBBE``, ``NO WAI``, or ``OIC``. The full expression syntax is then as follows:

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


The LOLCODE keyword for switches is ``WTF?``. The ``WTF?`` operates on ``IT`` as being the expression value for comparison. A comparison block is opened by ``OMG`` and must be a literal, not an expression. (A literal, in this case, excludes any YARN containing variable interpolation (``:{var}``).) Each literal must be unique. The ``OMG`` block can be followed by any number of statements and may be terminated by a ``GTFO``, which breaks to the end of the the ``WTF`` statement. If an ``OMG`` block is not terminated by a ``GTFO``, then the next ``OMG`` block is executed as is the next until a ``GTFO`` or the end of the ``WTF`` block is reached. The optional default case, if none of the literals evaluate as true, is signified by ``OMGWTF``.

::

    WTF?
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
  
.. _sssec:loop:

Loop
~~~~

Simple loops are demarcated with ``IM IN YR <label>`` and ``IM OUTTA YR <label>``.
Loops defined this way are infinite loops that must be explicitly exited with a GTFO break. Currently, the ``<label>`` is required, but is unused, except for marking the start and end of the loop.

Iteration loops have the form:

::

    IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>]
      <code block>
    IM OUTTA YR <label>


Where ``<operation>`` may be ``UPPIN`` (increment by one) or ``NERFIN`` (decrement by one).
That operation/function is applied to the ``<variable>``, which is temporary, and local to the loop.
The ``TIL <expression>`` evaluates the expression as a boolean: if it evaluates as false, the loop continues once more, if not, then loop execution stops, and continues after the matching ``IM OUTTA YR <label>``. The ``WILE <expression>`` is the converse: if the expression is true, execution continues, otherwise the loop exits.

.. _sssec:cast:

Casting
~~~~~~~

Operators that work on specific types implicitly cast parameter values of other types. If the value cannot be safely cast, then it results in an error.

An expression's value may be explicitly cast with the binary ``MAEK`` operator:

::

    MAEK <variable> [A] <type>

Where ``<type>`` is one of ``YARN`` or ``NUMBR``.

To explicitly re-cast a variable, you may create a normal assignment statement with the ``MAEK`` operator, or use a casting assignment statement as follows:

::

    <variable> R MAEK <variable> [A] <type>


.. _sssec:io:

Input/Output
~~~~~~~~~~~~

The print (to STDOUT or the terminal) operator is ``VISIBLE``. It has infinite arity and implicitly concatenates all of its arguments after casting them to YARNs. It is terminated by the statement delimiter (line end, comma, or single line comment). The output is automatically terminated with a carriage return (:)), unless the final token is terminated with an exclamation point (!), in which case the carriage return is suppressed.

::

VISIBLE <expression> [<expression> ...][!]

To accept input from the user, the keyword is

::

GIMMEH <variable>


which takes ``YARN`` for input and stores the value in the given variable.

