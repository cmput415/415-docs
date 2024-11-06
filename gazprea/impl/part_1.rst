.. _sec:part1:

Compiler Implementation — Part 1
================================

This section lists the portions of the *Gazprea* specification that must
be implemented to complete the part 1 of the compiler implementation.
All developers are advised to read the full specification for the
language prior to start the implementation of Part 1 because decisions
made while implementing Part 1 can make the implementation of Part 2
significantly more challenging. Thus, planning ahead for Part 2 is the
recommended strategy.

#. :ref:`sec:comments`
#. :ref:`sec:types`

   * :ref:`ssec:boolean`
   * :ref:`ssec:character`
   * :ref:`ssec:integer`
   * :ref:`ssec:real`
   * :ref:`ssec:tuple`

#. Type Support

   * :ref:`sec:typeQualifiers`

      * :ref:`ssec:typeQualifiers_var`
      * :ref:`ssec:typeQualifiers_const`

   * :ref:`sec:typePromotion`
   * :ref:`sec:typeCasting`
   * :ref:`sec:typeInference`
   * :ref:`sec:typedef`

#. :ref:`sec:statements`

   * :ref:`ssec:statements_assign`
   * :ref:`sec:declaration`
   * :ref:`sec:global`
   * :ref:`ssec:statements_block`
   * :ref:`ssec:statements_loop`

      * :ref:`ssec:statements_break`
      * :ref:`ssec:statements_continue`

   * :ref:`ssec:statements_cond`
   * :ref:`sec:streams`
   * :ref:`sec:function`
   * :ref:`sec:procedure`

#. :ref:`sec:expressions`

   * unary+, unary-, not

   * ^

   * \*,/,%

   * +,-

   * <,>,<=,>=,==,!=

   * and

   * or, xor

   * Variable references

   * Literal Values

   * Tuple reference

   * Function calls

#. :ref:`sec:errors`

   * SyntaxError

   * SymbolError

   * TypeError

   * AliasingError

   * AssignError

   * MainError

   * ReturnError

   * GlobalError

   * StatementError

   * CallError

   * DefinitionError

   * MathError
