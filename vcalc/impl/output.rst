Output
======

Output is to be written to a file specified on the command line. Your
compiler will be invoked with the following command:

::

     vcalc <input_file_path> <output_file_path>

You should open the file ``output_file_path`` and write to it. The
output file should be overwritten if it already exists.

Output content is standardized to ensure everyone can pass everyone’s
tests. Follow these specifications:

-  There *must* be a new line after each ``print`` statement’s printed
   value.

-  There *must not* be any trailing space after printed value and before
   the newline.

-  There *must* be an empty line at the end of your output.

-  There *must not* be spaces between the first and last number and the
   accompanying brackets in a vector.

-  There *must* be spaces between the numbers in a vector.

-  There *must not* be anything except spaces between the numbers in a
   vector.

| **Clarification:** Empty input should result in empty output.
  (:ref:`empty-input <clarify:empty-input>`)
| **Clarification:** Empty vectors print only brackets.
  (:ref:`empty-vector <clarify:empty-vector>`)
| **Clarification:** A vector with one value is only the brackets and
  the value. (:ref:`single-value-vector <clarify:single-value-vector>`)

