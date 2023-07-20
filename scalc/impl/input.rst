Input
=====

The input processed by your compiler will be in a file specified on the
command line. You will also receive a value signifying which mode your
compiler should be run in. The command to run your compiler will take
this form:

::

     scalc <mode> <input_file_path> <output_file_path>

Mode can be one of these four values:

-  ``risc``

-  ``x86``

-  ``arm``

-  ``interpreter``

You should open the file ``input_file_path`` and parse it. The input
file will be a valid scalc file.

