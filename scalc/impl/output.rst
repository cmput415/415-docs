Output
======

Output is to be written to a file specified on the command line. Your
compiler will be invoked with the following command:

::

     scalc <mode> <input_file_path> <output_file_path>

You should open the file ``output_file_path`` and write to it. The
output file should be overwritten if it already exists.

Output content is standardized to ensure everyone can pass everyone’s
tests. Follow these specifications:

-  Each number printed should be on its own line followed by a new line.

-  There *must* be a new line after each ``print`` statement’s printed
   value.

-  There *must not* be any trailing space after the final number and
   before the newline.

-  There *must* be an empty line at the end of your output.

**Clarification:** Empty input should result in empty output.
(:ref:`empty-input <clarify:empty-input>`)

