VCalc
=====

This assignment expands the simple calculator, *SCalc*, to build a vector
calculator called *VCalc*.
For *VCalc* you will build a compiler that generates `MLIR <https://mlir.llvm.org>`__. As *MLIR* is an IR infrastructure it supports many special purpose
intermediate representations called `dialects`.
You will target the `LLVM Dialect <https://mlir.llvm.org/docs/Dialects/LLVM/>`__
in this assignment.
All *MLIR* dialects must evenually be lowered to *LLVM IR*, which is the
common IR that the LLVM back-end uses to generate machine specific object code.
None of the assembly back ends that you built for *SCalc* need to be supported
for *VCalc*, because the LLVM back-end can support them all.
An interpreter is not necessary but can be a good way to ensure that your
grammar works as expected.

*VCalc* is a superset of *SCalc*. **All operations supported by SCalc
must be fully also supported by VCalc. All valid SCalc programs must run
in VCalc without modification.** (The only exceptions are variable names
in *SCalc* that are now reserved Keywords.) *VCalc* has the additional
features discussed in subsequent section.

.. toctree::
   :hidden:

.. toctree::
   :maxdepth: 3
   :caption: Language Specification
   :numbered:

   spec/keywords
   spec/vectors
   spec/range
   spec/generators
   spec/filters
   spec/expressions
   spec/statements
   spec/comments
   spec/type_checking
   spec/scoping

.. toctree::
   :maxdepth: 2
   :caption: Implementation

   impl/input
   impl/output
   impl/assertions
   impl/clarifications
   impl/deliverables
   impl/tips_hints
   impl/llvm_tips_hints
   impl/ast_tips_hints

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   start/layout
   start/clion_setup
   start/testing
