.. _sec:vcalc_architecture:

Architecture
============

You should write your compiler as a series of passes each with simple functionality. Do not implement your compiler as a single pass. As a minimum, your compiler should have individual passes that perform each of the following actions:

* Create an abstract syntax tree.
* Emit LLVM, SCF, Memref and Arith Dialects that can be lowered into LLVM IR.

These passes are also assessed against the architecture properties listed under Design in the :external+info:doc:`grading criteria <grading>`. Five of the six apply to *VCalc*.

Some VCalc designs do not carry over to Gazprea. Gazprea has multiple scalar types with promotion between them, nested tuple types, matrices and strings alongside vectors, assignable expressions other than plain identifiers, and routines callable before they are defined. A VCalc compiler can reasonably assume a single scalar type, a flat type tag, a one-dimensional vector representation, and one value per expression; none of these assumptions hold in Gazprea. Consider this when choosing how to represent types and values.
