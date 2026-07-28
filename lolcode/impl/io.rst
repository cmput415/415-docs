Input and Output
================

The input processed by your program will be in a file specified on the
command line:

::

     lolcode <source_file_path>

Input will be read from ``stdin`` and output is written to ``stdout``.
Error text is written to ``stderr``.

To run in batch mode, you can use file redirection:

::

   lolcode <source_file> < <input_file> > <output_file> 2> <error_file>


