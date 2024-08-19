MLIR Tips and Hints
===================

This section is likely to be constantly updated as new questions are
asked or useful things are found. You will be notified as appropriate.

-  It may be helpful to find out how ``clang`` translates equivalent *C*
   programs into *LLVM IR*. You can ask *clang* to output its generated
   *LLVM IR* via this command:

   ::

            clang -emit-llvm -S -c test.c

   Clang will sometimes optimise unused code away when we would really
   like to see what it’s doing. Consider changing to a different
   optimsation level or disabling it completely (``-O0``). As well, try
   printing intermediate values, the program will be forced to evaluate
   them.

   While you can’t use the text directly, it can give you an idea of
   what instructions are being created. The *LLVM* documentation is
   quite good. If you don’t immediately understand an instruction, the
   *LLVM* language reference is a great resource, as is our class
   forums. The instruction generation function is often found under the
   same name in the IR builder.

-  It can be a little harder to find programs that can emit MLIR.
   ``Tensorflow`` and ``flang`` (Fortran compiler) are two or the more well-known
   compilers that use MLIR, but both are admittedly niche. As an alternative,
   you can use the ``mlir::dump()`` method, which works on all MLIR operations
   including modules and functions. The MLIR framework provides several tools
   that can parse and work with files containing MLIR.
   In particular, ``mlir-opt`` can be used to run almost every optimization or
   transformation pass that exists on your MLIR output.
   For more information, execute ``mlir-opt --help`` after building and setting
   up MLIR.

-  While there appears to be copious quantities of *MLIR/LLVM* documentation,
   it can be frustatingly difficult to find documentation or examples of
   something you care about. One of the more effective tools is ``grep``,
   especially when used on the MLIR repository. ``git grep`` is automatically
   recursive, but because a lot of MLIR is generated at build time, ``grep -R``
   will search files in the build tree but outside the repository.

-  Sometimes *LLVM* generates unexpected (but correct) code. For
   example, requesting an integer cast can generate a multitude of
   instructions based on size of operands and signedness.

   For example, an unsigned cast from ``i1`` to ``i32`` will produce a
   ``zext`` (zero extend) instruction while a signed cast with the same
   types will produce a ``sext`` (sign extend) instruction, which is
   probably not what you want.

   Be careful of downcasting. Asking for a cast from a larger type
   integer type to a smaller integer type will only ever produce a
   ``trunc`` (truncate) instruction. This is *correct* but it’s not
   always what you want.

-  In order to perform some operations, it is a good idea to create a
   library of functions yourself to use internally. These functions
   compose what is called your runtime. These can be especially useful
   when dealing with vectors and may help to keep your generated code
   more easily readable.

   For example, rather than generating the necessary guards and final
   load used in vector indices, it may make more sense to create an
   indexing function to handle this for you, replacing all codegen with
   a simple function call.

   You can make sure there is no naming conflicts by either suffixing or
   prefixing your internal runtime variables or all of the program
   variables. *MLIR* and *LLVM* allow ``.`` characters in variable names while
   *VCalc* does not. This allows for easily guaranteed conflict-free
   names.

-  *MLIR* has an automatic way to verify modules for you. It can be a
   good idea to use it just before you output your code to make sure
   everything makes sense. This can be extremely helpful for noticing
   small errors. Here’s a basic invocation for your output using the
   verifier.

   ::

            #include "mlir/IR/Verifier.h"

            ...
            if (mlir::failed(mlir::verify(module)))
               std::cerr << "verification failed :-(" << std::endl;

-  **DO NOT USE MLIR TENSOR TYPES**. These are abstract types that have no
   memory layout or data pointers. This abstraction supports high level
   optimization but requires an involved lowering and bufferization process.
   In the same vein, we recommend you do not use the *MLIR* ``MemRefType``.
   This array type is backed by memory, but requires the ``memref`` dialect
   to allocate and manipulate instances of the type.

-  **DO NOT USE MLIR OR LLVM IR VECTOR TYPES**. These types are designed for
   Single Instruction Multiple Data (SIMD) processing which require
   specific version of processors. Using the LLVM IR vector types will
   result in a segmentation fault in architectures that do not support
   them. Not all lab machines support the *LLVM IR* vector.

-  You will need to divise your own vector type and method of storing
   data. One way is to use a linked list of structs with predefined
   integer arrays. Another is to ``malloc``/``free`` memory. Each has
   their own unique pros and cons.

-  You need to make a ``main`` function to insert code into to begin
   with. Here’s some boilerplate to get you rolling (note ``builder`` is type
   ``mlir::OpBuilder``):

   ::

            #include "mlir/Dialect/LLVMIR/LLVMDialect.h"
            #include "mlir/IR/BuiltinAttributes.h"
            #include "mlir/IR/TypeRange.h"
            #include "mlir/IR/Builders.h"
            #include "mlir/IR/BuiltinOps.h"
            #include "mlir/IR/Value.h"

            ...
            // For our purposes, the prototype for main can be "int main()"
            mlir::Type intType = builder->getI32Type();
            auto mainType = mlir::LLVM::LLVMFunctionType::get(intType, {}, false);
            mlir::LLVM::LLVMFuncOp mainFunc = builder->create<mlir::LLVM::LLVMFuncOp>(builder->getUnknownLoc(), "main", mainType);

            // Create an entry block and set the inserter.            
            mlir::Block *entry = mainFunc.addEntryBlock();
            builder->setInsertionPointToStart(entry);

-  When you run ``lli`` many common *C* functions are available, in
   particular you want ``printf`` to do your printing. To get
   ``printf``, you need to add it to your module similarly to adding
   your ``main``, but you do *not* define it. This corresponds to your
   *C*-style forward declaration and will make sure that llvm links
   ``printf`` into you executable. Here’s your boilerplate code where
   ``builder`` is type ``mlir::OpBuilder``:

   ::

            #include "mlir/Dialect/LLVMIR/LLVMDialect.h"
            #include "mlir/IR/TypeRange.h"
            #include "mlir/IR/Builders.h"

            ...
            // Create a function declaration for printf, the signature is:
            //   i32 (i8*, ...)
            auto llvmI8PtrTy = mlir::LLVM::LLVMPointerType::get(charType);
            llvmFnType = mlir::LLVM::LLVMFunctionType::get(intType, llvmI8PtrTy,
                                                           /*isVarArg=*/true);

            // Insert the printf declaration into the body of the parent module.
            builder->create<mlir::LLVM::LLVMFuncOp>(builder->getUnknownLoc(),
                                                    "printf", llvmFnType);

-  You may need to declare global constants in your module. The method
   for integers is similar to strings, but we show strings here because
   you will need it for use with ``printf``. For example, if I wanted to
   create a ``printf`` format string for newline (``builder`` is type
   ``mlir::OpBuilder``, ``context`` is type ``mlir::MLIRContext``, and ``loc``
   is type ``mlir::Location``):

   ::

            #include "mlir/Dialect/LLVMIR/LLVMDialect.h"
            #include "mlir/IR/BuiltinAttributes.h"

            ...
            // Create the global string "\n"
            mlir::Type charType = mlir::IntegerType::get(&context, 8);
            auto gvalue = mlir::StringRef("\n\0", 2);
            auto type = mlir::LLVM::LLVMArrayType::get(charType, gvalue.size());
            builder->create<mlir::LLVM::GlobalOp>(loc, type, /*isConstant=*/true,
                               mlir::LLVM::Linkage::Internal, "newline",
                               builder->getStringAttr(gvalue), /*alignment=*/0);

-  Calling functions is roughly the same in all places, but ``printf`` can be a
   little annoying to begin with because of the way it is  defined, so here is
   some more boilerplate code for calling that as well (
   ``builder`` is type ``mlir::OpBuilder``,
   ``module`` is type ``mlir::ModuleOp``,
   ``context`` is type ``mlir::MLIRContext``,
   and ``loc`` is type ``mlir::Location``):

   ::

            #include "mlir/Dialect/LLVMIR/LLVMDialect.h"
            #include "mlir/IR/Builders.h"
            #include "mlir/IR/BuiltinOps.h"
            #include "mlir/IR/Value.h"

            ...
            mlir::LLVM::GlobalOp global;
            if (!(global = module.lookupSymbol<mlir::LLVM::GlobalOp>("newline"))) {
                llvm::errs() << "missing format string!\n";
                return;
            }

            // Get the pointer to the first character in the global string.
            mlir::Value globalPtr = builder->create<mlir::LLVM::AddressOfOp>(loc, global);
            mlir::Value cst0 = builder->create<mlir::LLVM::ConstantOp>(loc,
                                                      builder->getI64Type(),
                                                      builder->getIndexAttr(0));

            mlir::Type charType = mlir::IntegerType::get(&context, 8);
            mlir::Value newLine = builder->create<mlir::LLVM::GEPOp>(loc,
                          mlir::LLVM::LLVMPointerType::get(charType),
                          globalPtr, mlir::ArrayRef<mlir::Value>({cst0, cst0}));

            auto printfFunc = module.lookupSymbol<mlir::LLVM::LLVMFuncOp>("printf");
            builder->create<mlir::LLVM::CallOp>(loc, printfFunc, newLine);


