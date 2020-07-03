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

#. 

   .. _assert:assign-streams:

   .. container::
      :name: assign-streams

      **assign-streams**:

   The streams constructors ``std\_output()`` and ``std\_input()`` *will
   not* be used in expressions. They must be assigned before use so that
   ``stream\_state`` can be checked later. For example, the following
   tests would be considered invalid:

   ::

            'a' -> std_output();
            character b;
            b <- std_input();

#. 

   .. _assert:const-arg:

   .. container::
      :name: const-arg

      **const-arg**:

   Procedure ``var`` arguments will not be passed ``const`` values. A
   ``var`` argument implies the value is mutable in the calling context,
   which a ``const`` value is not. See :ref:`sec:procedure` for more information. For
   example, the following tests would be considered invalid:

   ::

            procedure f(var integer i) {
              i = 1;
            }

            procedure main() returns integer {
              const integer i = 0;
              call f(i);
              return 0;
            }

#. 

   .. _assert:qualifier-init:

   .. container::
      :name: qualifier-init

      **qualifier-init**:

   Declarations using only qualifiers will be immediately initialised.
   If they were not, it would be impossible to infer their type, a
   necessary piece of information for use later in the AST. For example,
   the following tests would be considered invalid:

   ::

            var i;
            const i;

#. 

   .. _assert:safe-reals:

   .. container::
      :name: safe-reals

      **safe-reals**:

   No floating point operation will create a runtime error. This is a
   manifestation of the inability to standardise exception handling, not
   an extension to the spec forcing you to somehow fix floating point
   exceptions.
