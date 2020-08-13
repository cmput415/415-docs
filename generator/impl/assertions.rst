Assertions
==========

**ALL** input test cases will be valid. It can be a good idea to do
error checking for your own testing and debugging, but it is *not
necessary*. If you encounter what you think is undefined behaviour or
think something is ambiguous then *do* make a forum post about it to
clarify. While the generator is a relatively small spec, the latter
assignments *will not be*.

What does it mean to be valid input? The input must adhere to the
specification. The rules below give more in-depth explanation of
specification particulars.

#. 

   .. _assert:undef-behaviour:

   .. container::
      :name: undef-behaviour

      **undef-behaviour**:

   A test case *will not* take advantage of undefined behaviour.
   Undefined behaviour is functionality that does not have an outcome
   described explicitly by this specification.

#. 

   .. _assert:nonnegative-literals:

   .. container::
      :name: nonnegative-literals

      **nonnegative-literals**:

   All integer literals will be :math:`\geq 0`. For example, the
   following tests would be considered invalid:

   ::

            [i in 0..1 | -1];
            [i in -2..-1 | i];

#. 

   .. _assert:literal-size:

   .. container::
      :name: literal-size

      **literal-size**:

   All integer literals will fit in 31 unsigned bits. This means an
   integer literal can be anywhere in the range :math:`[0, 2^{31} - 1]`
   or :math:`[0, 2147483647]`. For example, the following tests would be
   considered invalid:

   ::

            [i in 0..1 | -1];
            [i in 0..1 | 2147483648];
            [i in 0..2147483648 | 0];
            [i in -1..1 | 0];

#. 

   .. _assert:nonnegative-exp:

   .. container::
      :name: nonnegative-exp

      **nonnegative-exp**:

   All exponents are :math:`\geq 0`. Exponents that are :math:`< 0`
   result in fractions (except when the base is 1). Given that the
   specification restricts generated numbers to be integers, it does not
   make sense to produce fractions. Therefore, you may assume that any
   exponent will be greater than or equal to zero, even if the base is
   1. For example, the following test would be considered in invalid:

   ::

            [i in 0..1 | 2 ^ (0 - 2)];

#. 

   .. _assert:expression-size:

   .. container::
      :name: expression-size

      **expression-size**:

   All expressions will result in a value that will fit in 32 signed
   bits. This means the result of an expression can be anywhere in the
   range :math:`[-2^{31}, 2^{31} - 1]` or :math:`[-2147483648, 2147483647]`. Any operation that results in underflow or overflow
   will render the input invalid. For example, the following tests would
   be considered invalid:

   ::

            [i in 0..1 | 2147483647 + 1];
            [i in 0..1 | 0 - 2147483647 - 2];

#. 

   .. _assert:zero-divide:

   .. container::
      :name: zero-divide

      **zero-divide**:

   No expression will contain a division by 0. The result of a division
   by zero is indeterminate so we will not handle it. For example, the
   following tests would be considered invalid:

   ::

            [i in 0..1 | 1 / 0];
            [i in 0..1 | 1 / (1 - 1)];

#. 

   .. _assert:simple-bounds:

   .. container::
      :name: simple-bounds

      **simple-bounds**:

   The bounds on the index variable will always be integer literals and
   never an expression. For example, the following test would be
   considered invalid:

   ::

            [i in (1-1)..1 | i];

#. 

   .. _assert:sane-bounds:

   .. container::
      :name: sane-bounds

      **sane-bounds**:

   The bounds on the index variable will always be such that
   :math:`\text{int_1} \leq \text{int_2}`. For example, the following test would
   be considered invalid:

   ::

            [i in 1..0 | i];

#. 

   .. _assert:matching-id:

   .. container::
      :name: matching-id

      **matching-id**:

   Any variable used in an expression will match the variable defined in
   the generator. For example, the following test would be considered
   invalid:

   ::

            [i in 0..1 | j];

#. 

   .. _assert:simple-whitespace:

   .. container::
      :name: simple-whitespace

      **simple-whitespace**:

   Whitespace is guaranteed to be a space, a tab, a carriage return, or
   a new line. Any other whitespace characters will render the input
   invalid. The following ANTLR rule will ensure you adhere to this:

   ::

            WS: [ \t\r\n]+ -> skip;
