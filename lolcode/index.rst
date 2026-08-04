LOLCODE
=======

The goal of this assignment is to implement a **LL1** Parser for a subset of the
esoteric language called ``LOLCODE <https://lolcode.org>_``.
This language is simple enough that you will not need advanced lookahead.
Your parser will use the ANTLR4 lexer to generate a token stream, which can then
be used to generate an AST.
You must also create an :term:`interpreter` for LOLCODE by walking your AST
using a visitor pattern.

Your parser must do basic error detection, but it need not do error recovery,
i.e. it does not need to try to continue parsing once an error is encountered.
While your ANTLR4 grammar file only needs lexical rules defined, you may find
it helpful to also write the parser rules that you will implement.
You are allowed to use any internal AST representation that you wish.
It does not need to be persisted, since the in-memory representation is all
that is needed for the interpreter.

The canonical "Hello World" program in LOLCODE is:

::

    HAI  BTW Our first program!
        VISIBLE "Hello Wurld, LOL!"
    KTHXBYE

This snippet reveals important basic principles of the language:

- LOLCODE is *imperative* (statement oriented)

- LOLCODE is *block structured* as seen by the ``HAI``/``KTHXBYE`` bracketing.

- white space is not important, *except* that newline is used as a statement terminator

As a more interesting example, the following LOLCODE program implements the
simple "Guessing Game":

::

   HAI
       I HAS A answer ITZ 42
       I HAS A guess
       VISIBLE "Has guess?"

       OBTW infinite loop TLDR
       IM IN YR loop
          GIMMEH guess                  BTW input is a string
          MAEK guess A NUMBR            BTW cast

          BOTH SAEM guess AN answer, O RLY?
             YA RLY
                 VISIBLE "Score!"
                 GTFO                   BTW break
             MEBBE BOTH SAEM guess AN SMALLR OF guess AN answer
                 VISIBLE "Moar!"
             NO WAI                     BTW else
                 VISIBLE "2 Much!"      
          OIC
       IM OUTTA YR loop
    KTHXBYE
   
Our simplified version of LOLCODE has integer and string variables,
conditionals, loops, I/O, and various integer
:term:`expressions <expression>`. The full version of
LOLCODE has file I/O, functions, and more advanced expressions and operations.
We provide the simplified spec in this document, however, since it is derived
from the full spec at <https://lolcode.org>, you may find it adds additional
context.
  
.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 3
   :caption: Language Specification
   :numbered:

   spec/formatting
   spec/variables
   spec/expressions
   spec/statements

.. toctree::
   :maxdepth: 2
   :caption: Implementation

   impl/deliverables
   impl/io
   impl/assertions
   impl/clarifications
   impl/tips_hints

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

.. |expectedForm| image:: assets/images/scalc-class.png
