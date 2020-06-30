Generator Assignment
====================

For this assignment you will be building a parser for a number
generator. The generator will produce a series of numbers through an
expression. Your task is to parse the generator statement, interpret it,
and print the numbers that should be produced by the generator. You will
be using *ANTLR4* to generate a **lexer** and **parser** for your
interpreter. You will then implement the interpreter in *C++*.
Documentation and tutorials for *ANTLR4* can be found here `Antlr4
documentation <https://github.com/antlr/antlr4/blob/master/doc/index.md>`__.

.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 3
   :caption: Language Specification
   :numbered:

   spec/keywords
   spec/integer_lit
   spec/identifiers
   spec/expression
   spec/generator

.. toctree::
   :maxdepth: 2
   :caption: Implementation

   impl/input
   impl/output
   impl/assertions
   impl/clarifications
   impl/deliverables
   impl/tips_hints

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   start/get_project
   start/clion_setup
   start/testing