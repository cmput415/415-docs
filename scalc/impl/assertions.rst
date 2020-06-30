Assertions
==========

**ALL** input test cases will be valid. It can be a good idea to do
error checking for your own testing and debugging, but it is *not
necessary*. If you encounter what you think is undefined behaviour or
think something is ambiguous then *do* make a forum post about it to
clarify.

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

            int i = -1;

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

            int i = 2147483648;

#. 

   .. _assert:expression-size:

   .. container::
      :name: expression-size

      **expression-size**:

   All expressions will result in a value that will fit in 32 signed
   bits. This means the result of an expression can be anywhere in the
   range :math:`[-2^{31}, 2^{31} - 1]` or :math:`[-2147483648, 2147483647]`.
   Any operation that results in underflow or overflow
   will render the input invalid. For example, the following tests would
   be considered invalid:

   ::

            int i = 2147483647 + 1;
            int j =  0 - 2147483647 - 2;

#. 

   .. _assert:zero-divide:

   .. container::
      :name: zero-divide

      **zero-divide**:

   No expression will contain a division by 0. The result of a division
   by zero is indeterminate so we will not handle it. For example, the
   following tests would be considered invalid:

   ::

            int i = 1 / 0;
            int j = 1 / (1 - 1);

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

