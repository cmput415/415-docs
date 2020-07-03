.. _sec:assertions:

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

   .. _assert:opened-comments:

   .. container::
      :name: opened_comments

      **opened-comments**:

   Block comments will be opened. Not opening a block comment will cause
   ANTLR to encounter a lost ``*/`` as well as causing a stream of word
   tokens starting from where the ``/*`` token should be. For example,
   the following tests would be considered invalid:

   ::

            integer i = 0;
            I'm a closed comment, but I'm never opened... */
            integer j = i + 1;

#. 

   .. _assert:closed-comments:

   .. container::
      :name: closed-comments

      **closed-comments**:

   Block comments will be closed. Not closing a block comment will have
   ANTLR consume every token in the file, rendering the rest of the file
   useless. For example, the following tests would be considered
   invalid:

   ::

            integer i = 0;
            /* I'm an opened comment, but I'm never closed...
            integer j = i + 1;
