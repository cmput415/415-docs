Output
======

Output is to be written to a file specified on the command line. Your
compiler will be invoked with the following command:

::

     vcalc <input_file_path> <output_file_path>

You should open the file ``output_file_path`` and write to it. The
output file should be overwritten if it already exists.

The output of your compiler is the *LLVM IR* that corresponds to the given
input program. The output file can be used as input to ``llc``, for example,
which compiles *LLVM IR* input into assembly language for a specified machine.
From there the tools you used in *SCalc* can be used to create an executable.


