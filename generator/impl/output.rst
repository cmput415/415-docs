Output
======

Output is to be written to a file specified on the command line. Your
interpreter will be invoked with the following command:

::

     generator <input_file_path> <output_file_path>

You should open the file ``output_file_path`` and write to it. The
output file should be overwritten if it already exists.

Output content is standardized to ensure everyone can pass everyone’s
tests. Follow these specifications:

-  All generated numbers should be printed on the same line with a
   single space separating the numbers.

-  There *must* be a new line after each generator’s output.

-  There *must not* be any trailing space after the final number and
   before the newline.

-  There *must* be an empty line at the end of your output (a result of #2).

**Clarification:** Empty input should result in empty output.
(:ref:`empty-input <clarify:empty-input>`)

Example input (3 lines):
::

     [i in 1..10| i];
     [x in 0..3| x-1];
     [x in 1..4| 10];

Expected Output (4 lines since each generator is newline terminated.):
::

   1 2 3 4 5 6 7 8 9 10
   -1 0 1 2
   10 10 10 10

Depending on the text editor a file is viewed in, the final empty line may not be
rendered (like the viewer above). To be sure your test cases adhere to the spec, make use
of the `415 Tester <https://github.com/cmput415/Tester>`_ which ensures that generated and expected 
output match to every single byte.
