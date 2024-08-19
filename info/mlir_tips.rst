MLIR Tips and Hints
===================

MLIR tips
---------

* It may be helpful to find out how clang translates equivalent C programs into LLVM IR. You can ask
  clang to output its generated LLVM IR via this command:

  .. code-block:: bash

     clang -emit-llvm -S -c test.c

* Clang will sometimes optimize unused code away when we would really like to see what it's doing.
  Consider changing to a different optimization level or disabling it completely (-O0). Additionally,
  try printing intermediate values; the program will be forced to evaluate them. 

  While you can't use the text directly, it can give you an idea of what instructions are being
  created. The LLVM documentation is quite good. If you don't immediately understand an instruction,
  the LLVM language reference is a great resource, as are our class forums. The instruction
  generation function is often found under the same name in the IR builder.

* It can be a little harder to find programs that can emit MLIR. TensorFlow and flang (Fortran
  compiler) are two of the more well-known compilers that use MLIR, but both are admittedly niche.
  As an alternative, you can use the ``mlir::dump()`` method, which works on all MLIR operations
  including modules and functions. The MLIR framework provides several tools that can parse and work
  with files containing MLIR. In particular, ``mlir-opt`` can be used to run almost every
  optimization or transformation pass that exists on your MLIR output. For more information, execute
  ``mlir-opt --help`` after building and setting up MLIR.

* While there appears to be copious quantities of MLIR/LLVM documentation, it can be frustratingly
  difficult to find documentation or examples of something you care about. One of the more effective
  tools is grep, especially when used on the MLIR repository. ``git grep`` is automatically
  recursive, but because a lot of MLIR is generated at build time, ``grep -R`` will search files in
  the build tree but outside the repository.

* Sometimes LLVM generates unexpected (but correct) code. For example, requesting an integer cast
  can generate a multitude of instructions based on size of operands and signedness. For instance,
  an unsigned cast from i1 to i32 will produce a zext (zero extend) instruction while a signed cast
  with the same types will produce a sext (sign extend) instruction, which is probably not what you
  want.

  Be careful of downcasting. Asking for a cast from a larger integer type to a smaller integer type
  will only ever produce a trunc (truncate) instruction. This is correct but it's not always what
  you want.

MLIR Dialect Tips
=================

You and your team member(s) will face an important decision regarding which dialects to use and to
what extent. The endorsed dialects ``llvm``, ``scf``, ``memref``, ``func`` and ``arith`` exist at various
"heights" in the MLIR tree; interactions between types and operations in each dialect can be
surprising. Despite there being many subsets of the 5 dialects to choose from we do not recommend choosing
arbitrarily.

Recommended options:

1. llvm
2. llvm + scf
3. llvm + scf + memref + arith + func

LLVM
----
* The LLVM dialect is well tested on the 415 assignments. All years previous to Fall 2024 have used
  either LLVM or the LLVM dialect exclusively.

* All control flow in both vcalc and gazprea can be implemented entirely using the llvm dialect.
  The LLVM Dialect lets you create basic blocks, lay out branches, jumps and returns explicitly.
  
* Functions can be declared and/or defined in the MLIR module. A great utility header
  ``"mlir/Dialect/LLVMIR/FunctionCallUtils.h"`` gives some convenient interfaces for working with functions.
  Included are methods to declare malloc and free out of the box.

* Functions that are declared can find definitions at runtime from the dynamically
  linked C library included in your projects. In general, the llvm dialect types are easier
  to pass through to runtime funtions. 

* LLVM Struct types allow you to create aggregate data structures from other llvm dialect types.
  A custom struct type can be constructed:

  .. code-block:: cpp

     mlir::ArrayRef<mlir::Type> types; // a collection of scalar types 
     mlir::Type struct_type =
         mlir::LLVM::LLVMStructType::getLiteral(&ctx::context, types);

* All vectors and matrices can be implemented within the LLVM dialect.

SCF
---

* ``scf`` ops such as ``scf.if``, ``scf.for`` and ``scf.while`` offer convenient, modular interfaces
  for creating control flow that abstract away the work of manually laying out basic blocks.
  In contrast, the ``llvm`` dialect offers fine-grained control over how basic blocks are arranged and connected.

* **All scf ops allow only one basic block in their body**. As a consequence, ``scf`` ops cannot be mixed with ``llvm``
  control flow. Under this restriction, for example, nesting an ``llvm`` while loop made with basic
  blocks inside an ``scf.if`` is impossible. This imposes that intra-procedural control flow be
  implemented "all or nothing" with either ``scf`` or ``llvm``.

Memref
------

* ``memref`` ops such as ``alloc`` and ``alloca`` may be used as an alternative to ``llvm.alloca`` and ``malloc``.
  A memref op has more meta-data surrounding the buffer. The stride and shape of each dimension is built into the type,
  and can be easily accessed using a ``memref.dimOp``. The trade-off is that the corresponding ``C`` type needed to
  "catch" a memref value on the receiving side of a function call is a large struct compared to a simple void pointer as in malloc.

* For example, an ``alloc`` of one dimension and type float32 has the following corresponding C struct:

  .. code-block:: c

     typedef struct {
       float *alloc;
       float *align;
       uint64_t offset;
       uint64_t sizes[1];    // single dim size
       uint64_t strides[1];  // single dim stride
     } memref_vector_float_t;

* The need to create a vector from a previously computed `mlir::Value` is common.
  For example, creating a range from ``2..7`` involves using the result of a subtraction.
  To do this, a specific memref type must be created which has a dynamic size.

  Creating a memref type for a vector of floats.

  .. code-block:: c

     mlir::Type floatType = mlir::Float32Type::get(&context);
     mlir::MemRefType floatVecTy = mlir::MemRefType::get(mlir::ShapedType::kDynamic, floatType);

* memref is relatively high in the dialect tree. As a consequence, passing an allocOp through an llvm function
  parameter will not lower correctly. As a result, using memref requires also using the func dialect.  

* Similar to the previous point, memref types are indexed using the Index type from the ``arith`` dialect.

Arith
-----

* If using memref, the only type needed from this dialect is the ``Index`` type. Otherwise ``arith``
  is not necessary.

* The underlying representation of the ``Index`` type is a 64-bit signed integer.

* With caution, i32 type Integers can be cast into index types and vice versa:

  .. code-block:: 

     mlir::Value integer = builder->create<mlir::LLVM::ConstantOp>(
                   loc, builder->getI32Type(), 1024);
     mlir::Value index = builder->create<mlir::arith::IndexCastOp>(
                   loc, builder->getIndexType(), integer);
     integer = builder->create<mlir::arith::IndexCastOp>(
                   loc, builder->getI32Type(), integer);

Func
----

* The func dialect is quite small and self-explanatory. The advantage over
  llvm functions is that the func dialect can handle types from other high
  level dialects like memref.

* It is useful to be able to lookup a function you have already declared.
  
  .. code-block:: c

     module.lookupSymbol<mlir::func::FuncOp>("vectorAdd");