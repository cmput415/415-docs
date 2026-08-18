VCalc
=====

In this assignment you will build a vector calculator called *VCalc*.
For *VCalc* you will build a compiler that generates `MLIR <https://mlir.llvm.org>`__.
As *MLIR* is an IR infrastructure it supports many special purpose
intermediate representations called `dialects`.
You will target the `LLVM Dialect <https://mlir.llvm.org/docs/Dialects/LLVM/>`__
in this assignment.
All *MLIR* dialects must evenually be lowered to *LLVM IR*, which is the
common IR that the LLVM back-end uses to generate machine specific object code.
An interpreter is not necessary but can be a good way to ensure that your
grammar works as expected.


.. toctree::
   :hidden:

.. toctree::
   :maxdepth: 3
   :caption: Language Specification
   :numbered:

   spec/keywords
   spec/comments
   spec/identifiers
   spec/booleans
   spec/integers
   spec/vectors
   spec/range
   spec/generators
   spec/filters
   spec/expressions
   spec/statements
   spec/scoping
   spec/type_checking

.. toctree::
   :maxdepth: 2
   :caption: Implementation

   impl/architecture
   impl/input
   impl/output
   impl/assertions
   impl/clarifications
   impl/deliverables
   impl/tips_hints
   impl/llvm_tips_hints
   impl/ast_tips_hints
