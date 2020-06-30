VCalc
=====

This assignment expands the simple calculator, *SCalc*, to build a
vector calculator called *VCalc*. For *VCalc* you need only build an
*LLVM IR* back end. None of the assembly back ends that you built for
*SCalc* need to be supported for *VCalc*. An interpreter is not
necessary but can be a good way to ensure that your grammar works as
expected.

*VCalc* is a superset of *SCalc*. **All operations supported by SCalc
must be fully also supported by VCalc. All valid SCalc programs must run
in VCalc without modification.** (The only exceptions are variable names
in a *SCalc* that are now reserved Keywords.) *VCalc* has the additional
features discussed in subsequent section.

.. toctree::
   :hidden:

   self
   changelog

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
   impl/ast_tips_hints

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   start/layout
   start/clion_setup
