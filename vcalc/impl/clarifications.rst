Clarifications
==============

These clarifications are meant to add more information to the
specification without cluttering it.

#. 

   .. _clarify:empty-input:

   .. container::
      :name: empty-input

      **empty-input**:

   Empty input should result in empty output. This is in keeping with
   all of the output rules defined. There are no ``print`` statements so
   there would be no numbers, newlines or output of any kind. All that
   you are left with is a single empty line, which matches "*should* be
   an empty line at the end of your output".

#. 

   .. _clarify:empty-vector:

   .. container::
      :name: empty-vector

      **empty-vector**:

   Empty vectors print only brackets. This is in keeping with all of the
   output rules defined. There are no integers to print between the
   brackets, so there is no values nor spaces to print. For example:

   ::

            []

#. 

   .. _clarify:single-value-vector:

   .. container::
      :name: single-value-vector

      **single-value-vector**:

   A vector with one value is only the brackets and the value. This is
   in keeping with all of the output rules defined. There is only one
   integer. There is no space between the first bracket and the integer
   and no space between the integer and the second bracket. For example:

   ::

            [1]

