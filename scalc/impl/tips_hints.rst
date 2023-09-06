Tips and Hints
==============

-  Review the `Tips and
   Hints <https://webdocs.cs.ualberta.ca/%7Ec415/generator/>`__ from the
   generator assignment: much of it applies to this assignment as well.
   In particular, the style and design sections are necessary.

-  Write tests *before* you implement the things they will test. The
   testing script provided is designed to handle failed test cases. You
   can reduce output in the testing tool by passing the ``-q`` flag.

-  As with the generator assignment, the ANTLR visitor pattern is best
   for implementing the interpreter.

-  The RISC-V, ARM, and x86 compilers can be built using either the
   visitor or the listener pattern. The listener may be more appropriate
   so it is the suggested method.

-  A single listener or visitor should be able to handle the x86, RISC-V,
   and ARM code generation. All that should change is the templated
   strings.

-  In addition to the `previous
   tips <https://webdocs.cs.ualberta.ca/%7Ec415/generator/>`__, here’s
   how to stay stylish in this assignment:

   -  There is no specified syntax guide for use with *inja*, thus you
      **could** write your strings in any style that you choose. I
      suggest you use `implicit string
      concatenation <https://softwareengineering.stackexchange.com/q/254984>`__
      to delineate your strings. For example, this may be a format
      string for literal division:

      ::

                   std::string literalDivision =
                     "\n  # Div.\n"
                     "  addi  t0, zero, {{ dividend }} # Set dividend.\n"
                     "  addi  t1, zero, {{ divisor }}  # Set divisor.\n"
                     "  div   t2, t0, t1               # Divide.\n"

-  This assignment will be extended to build a calculator that handles
   vectors in the next assignment. For that assignment you will need to
   do type checking. Therefore you are advised to:

   -  Read that assignment now.

   -  Include type checking in this solution even though you are only
      required to handle integers in this assignment.

-  You are allowed to use RISC-V pseudo-instructions.


