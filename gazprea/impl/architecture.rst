.. _sec:architecture:

Architecture
============

You should write your compiler as a series of passes each with simple functionality. Do not implement your compiler as a single pass. As a minimum, your compiler should have individual passes that perform each of the following actions:

* Create an abstract syntax tree.
* Define symbols and ensure that symbols can be referenced in the locations they are used. These actions may be performed by two separate passes.
* Propagate type information through expressions and perform static type checking. These actions may be performed by two separate passes.
* Emit LLVM, SCF, Memref and Arith Dialects that can be lowered into LLVM IR.

Your compiler should use a symbol table to track symbol definitions and scopes.

These passes are also assessed against the architecture properties listed under Design in the `grading criteria <https://cmput415.github.io/415-docs/info/grading.html>`_. All six properties apply to *Gazprea*.
