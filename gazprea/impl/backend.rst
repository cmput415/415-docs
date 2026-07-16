.. _sec:backend:

Backend
=======

You don’t need to implement an interpreter for Gazprea. You only need to
implement a *MLIR* code generator that outputs *LLVM IR*.

.. _ssec:representing_values:

Representing Values
-------------------

When you emit MLIR you must decide *how a value lives*: as an SSA value that is
defined once, or as a slot in memory that you load from and store to. Pick one deliberately.

.. note::

   **In practice.** The memory model (``alloca`` / ``load`` / ``store`` +
   ``mem2reg``) is standard for imperative, systems-style languages with an
   explicit, language-defined memory layout, like C. Value-semantic ``tensor``
   representations are favored at the high level by array- and math-focused
   compilers like Fortran and Tensorflow.

**The memory model.** Give every value a slot: reads are loads, writes are stores.
The mutable state lives in memory and the optimizer's ``mem2reg`` promotion turns the slots back into SSA
registers for you. A scalar declaration is an ``alloca``, a read a ``load``, an
assignment a ``store``:

::

   // var integer n = 42;  then  n = n + 1;
   %n = memref.alloca() : memref<i32>
   memref.store %c42, %n[] : memref<i32>
   %0 = memref.load %n[] : memref<i32>
   %1 = arith.addi %0, %c1 : i32
   memref.store %1, %n[] : memref<i32>

It pairs naturally with unstructured ``cf``: because the state is in memory,
``break`` / ``continue`` / ``return`` are ordinary branches — to the loop's exit
block, its latch, and the function exit — with nothing threaded through them and
no analysis of which variables cross a construct. 

**The value (SSA) model.** Map each variable name to its *current* SSA value: a
read is a lookup, an assignment produces a new value and rebinds the name. There
are no slots and no loads or stores; bufferization introduces memory later,
downstream of your emitter. The one hard case is a *merge*: after an ``if``, a
variable set on only one branch still needs a single value afterward. The
structured ``scf`` ops hand you this by *yielding* merged values as region results
(``scf.if`` results, ``scf.for`` / ``scf.while`` ``iter_args``) rather than making
you place a merge:

::

   // if (c) { x = 1; } else { x = 2; }   -- x lives after the if
   %x = scf.if %c -> (i32) {
     scf.yield %c1 : i32
   } else {
     scf.yield %c2 : i32
   }

``scf`` requires you to declare the set of values a region carries (those it
modifies that are still needed afterward). ``scf`` also has no early exit — a region runs
to its ``scf.yield`` — so Gazprea's ``break``, ``continue``, and ``return`` need a
way to be represented *inside* a structured region; work out how before you commit
to this model.

.. Warning::
   Avoid emitting unstructured ``cf`` blocks and
   placing the phi / block-argument merges yourself.

.. Warning::
   The SSA model is the more difficult of the two to implement, but can allow for more 
   optimization to occur.

.. _ssec:representing_arrays:

Representing Arrays and Aggregate Types
---------------------------------------

Arrays, matrices, and vectors can live in memory or as values, the same choice as
for scalars, but their interaction with tuples/structs is a complication.

Vector representation
~~~~~~~~~~~~~~~~~~~~~

A ``{ptr, len, capacity}`` struct or similar is the standard way to implement growable memory.

.. Note::
   For performance marks, consider how your vector grows.

Array representation
~~~~~~~~~~~~~~~~~~~~

Three options, differing in ease of implementation and
optimization potential.

- **A** ``memref`` **(memory model).** Allows optimization via ``linalg.generic``, but
  gives up
  fusion: a chain like ``a * b + a`` is two loops with an intermediate buffer.

- **A** ``tensor`` **(value model).**
  Element assignment ``v[i] = e`` is a ``tensor.insert`` that *yields a new value*
  you rebind, threaded exactly like a scalar. Fusion is available — a pure
  elementwise chain of ``tensor`` values fuses into one loop — but it must happen
  while the arrays are still ``tensor`` (once bufferized they are memory).

- **A** ``{ptr, len, cap}`` **struct**: The simplest option, uniform with vectors.
  You give
  up the standard-dialect machinery — no ``linalg``, no ``memref`` / ``tensor``
  passes.

Allocation, ownership, and freeing for all three are covered in
:ref:`ssec:backend_memory`.

Array fields inside structs and tuples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A struct or tuple may have an
array-typed field — ``struct s1 (integer i, real r, integer[10] iv)``,
``tuple(integer, real, integer[10])``. A standalone array can use any of the three above
representations; an array within a struct must exist as a valid representation
inside the aggregate or be lifted out of it. 

.. Warning::
   ``!llvm.struct<memref>`` and ``!llvm.struct<tensor>`` will not lower, only an 
   LLVM-typed field may nest inside an ``llvm.struct``. A ``{ptr, len, cap}`` 
   struct *is* an LLVM type and nests freely.

**Option 1 — one representation everywhere.** Use a ``{ptr, len, cap}`` or ``{ptr, len}`` struct for
**every** sequence: arrays, vectors, strings, matrices. A struct or tuple is then
an ``!llvm.struct`` of its fields, and an array field is just a ``{ptr, len}``
member — nesting is free and has no special case.

**Option 2 — split by mutability.** Represent arrays and matrices as
``memref`` or ``tensor``. Because a ``memref`` / ``tensor`` cannot nest in an ``!llvm.struct``, an array that
appears as an aggregate field is handled by **SoA decomposition**: the aggregate is
split into its leaves, and each array field becomes its own top-level ``memref`` /
``tensor`` value threaded alongside the others rather than a member of one struct
object. A ``{i, r, iv}`` struct is carried as the parallel leaves ``i32``,
``f64``, ``memref<10xi32>``; there is no single aggregate value. Vectors, being
``{ptr, len, cap}``, still nest normally. The cost is two sequence representations
plus the decomposition machinery — a 1:N type conversion that splits aggregates
into leaves and carries them across call, return, and loop boundaries. The payoff
is greater array and matrix optimization.

.. Warning::
   This is lots of work to implement.

.. Note::
   Under Struct of Arrays (SoA) decomposition, the following transformation occurs:
   ::
      tuple(integer, real[10], integer[2]) data;
      data.2[5] = 4;

   becomes
   ::
      integer data_1;
      real[10] data_2;
      integer[2] data_3;
      data_2[5] = 4;
   
   In the resulting program, there are no arrays in aggregates.


.. _ssec:backend_memory:

Memory Management
-----------------

It is important that you are able to automatically free and allocate memory for
arrays when they enter and exit scope. You could allocate them on the stack,
but this could be problematic if the arrays are very large.
It is likely safer to use ``malloc`` and ``free`` for these purposes.
This may be done in either your runtime or directly within MLIR.

Below is an example of how to use ``malloc`` and ``free`` within MLIR using the LLVM dialect:

::

  module {
    llvm.func @malloc(i32) -> !llvm.ptr<i8>
    llvm.func @free(!llvm.ptr<i8>)
    llvm.func @main() -> i32 {
      %0 = llvm.mlir.constant(128 : i32) : i32
      %1 = llvm.call @malloc(%0) : (i32) -> !llvm.ptr<i8>
      llvm.call @free(%1) : (!llvm.ptr<i8>) -> ()
      %c0_i32 = llvm.mlir.constant(0 : i32) : i32
      llvm.return %c0_i32 : i32
    }
  }

It is important that the code generated by your compiler has no memory leaks,
and that all memory is freed as it leaves scope.

.. _ssec:backend_runtime:

Runtime Libraries
-----------------

If you make a runtime library, the runtime library must be implemented
in a runtime directory (``runtime``). Beware that in C++ there is additional
name mangling that occurs to allow class functions. Thus, we recommend
that all runtime functions should be written in C and not in C++. There
is a Makefile in the ``runtime`` folder designed to turn all ``*.c`` and
``*.h`` pairs into part of the unified runtime library ``libruntime.a``.
An example of how to make a runtime function is provided below.

``functions.c``

::

       #include "functions.h"

       uint64_t factorial(uint64_t n) {
           uint64_t fact = 1;

           while (n > 0) {
               fact *= n;
               n--;
           }

           return fact;
       }

``functions.h``

::

       #pragma once

       #include <stdint.h>

       uint64_t factorial(uint64_t n);

If your compiler was compiling the following input

::

       3! + (2 + 7)!

Here is how to call the function in the LLVM dialect of MLIR:

``MLIR src``

::

   module {
     // This makes the function available for calling
     llvm.func @factorial(i64) -> i64

     llvm.func @main() -> i32 {
       // Calls factorial with the constant 3 as an argument
       %0 = llvm.mlir.constant(3 : i64) : i64
       %1 = llvm.call @factorial(%0) : (i64) -> (i64)

       // Adds 2 and 7 together
       %2 = llvm.mlir.constant(2 : i64) : i64
       %3 = llvm.mlir.constant(7 : i64) : i64
       %4 = llvm.add %2, %3 : i64

       // Calls factorial with the result of 2+7
       %5 = llvm.call @factorial(%4) : (i64) -> (i64)

       // Adds the result of 3! with (2+7)!
       %6 = llvm.add %1, %5 : i64

       // Done, return 0
       %c0_i32 = llvm.mlir.constant(0 : i32) : i32
       llvm.return %c0_i32 : i32
    }
  }

