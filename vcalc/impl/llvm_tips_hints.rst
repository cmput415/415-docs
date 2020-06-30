LLVM Tips and Hints
===================

This section is likely to be constantly updated as new questions are
asked or useful things are found. You will be notified as appropriate.

-  It may be helpful to find out how *clang* translates equivalent *C*
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

   LLVM IR is not static and can change between versions. Often, things
   are not too different so using a different version will not affect
   you. If things are not working out and you would like to be
   absolutely sure, you can build *clang* yourself or use the executable
   that has been already built for you on the CSC lab machines (need to
   be sourcing our setup files). We operate from the release_60 branch
   in the `c415 repository <https://github.com/cmput415/clang>`__. The
   version command thus produces:

   ::

            clang version 6.0.1 (https://github.com/cmput415/clang.git 2f27999df400d17b33cdd412fdd606a88208dfcc) (https://github.com/cmput415/llvm.git 2c9cf4f65f36fe91710c4b1bfd2f8d9533ac01b5)
            Target: x86_64-unknown-linux-gnu
            Thread model: posix
            InstalledDir: /cshome/c415/415-resources/llvmi/bin

-  The *LLVM* interface has its own small optimisations built in. Often
   this is only instruction reduction. Be aware that you may find code
   that you emitted to be missing. The easiest to see case is constant
   folding. If two constants are operated on, the operation will be
   completed before emitting any code and instead you will see only
   their result as a constant.

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
   variables. *LLVM IR* allows ``.`` characters in variable names while
   *VCalc* does not. This allows for easily guaranteed conflict-free
   names.

-  Most instructions generated give you the opportunty to name the
   result if you want. While you don’t need to, it can help you debug
   when things are going wrong.

-  *LLVM* has an automatic way to verify modules for you. It can be a
   good idea to use it just before you output your code to make sure
   everything makes sense. This can be extremely helpful for noticing
   small errors. Here’s a basic invocation for your output using the
   verifier.

   ::

            #include "llvm/IR/Verifier.h"
            #include "llvm/Support/raw_os_ostream.h"
            #include <iostream>
            ...
            llvm::raw_os_ostream llOut(outStream);
            llvm::raw_os_ostream llErr(std::cerr);
            llvm::verifyModule(mymodule, &llErr);
            myModule.print(llOut, nullptr);

-  **DO NOT USE LLVM IR VECTOR TYPES**. These types are designed for
   Single Instruction Multiple Data (SIMD) processing which require
   specific version of processors. Using the LLVM IR vector types will
   result in a segmentation fault in architectures that do not support
   them. Not all lab machines support the *LLVM IR* vector.

-  You will need to divise your own vector type and method of storing
   data. One way is to use a linked list of structs with predefined
   integer arrays. Another is to ``malloc``/``free`` memory. Each has
   their own unique pros and cons.

-  You need to make a ``main`` function to insert code into to begin
   with. Here’s some boilerplate to get you rolling:

   ::

            #include "llvm/IR/DerivedTypes.h"
            #include "llvm/IR/TypeBuilder.h"
            #include "llvm/Support/Cast.h"
            ...
            // Create main function, returns int, takes no args.
            llvm::FunctionType *mainTy = llvm::TypeBuilder<int(), false>::get(ctx);
            auto *mainFunc = llvm::cast<llvm::Function>(mod.getOrInsertFunction("main", mainTy));

            // Create an entry block and set the inserter.
            llvm::BasicBlock *entry = llvm::BasicBlock::Create(ctx, "entry", mainFunc);
            ir.SetInsertPoint(entry);

-  When you run ``lli`` many common *c* functions are available, in
   particular you want ``printf`` to do your printing. To get
   ``printf``, you need to add it to your module similarly to adding
   your ``main``, but you do *not* define it. This corresponds to your
   *c*-style forward declare and will make sure that llvm links
   ``printf`` into you executable. Here’s your boilerplate code where
   ``module`` is your ``llvm::Module``:

   ::

            #include "llvm/IR/Attributes.h"
            #include "llvm/IR/DerivedTypes.h"
            #include "llvm/IR/Function.h"
            #include "llvm/IR/TypeBuilder.h"
            #include "llvm/Support/Cast.h"
            ...
            // Declare printf. Returns int, takes string and variadic args.
            llvm::FunctionType *printfTy = llvm::TypeBuilder<int(char *, ...), false>::get(ctx);
            auto *printfFunc = llvm::cast<llvm::Function>(module.getOrInsertFunction("printf", fTy));

            // Add the suggested argument attributes.
            printfFunc->addAttribute(1u, llvm::Attribute::NoAlias);
            printfFunc->addAttribute(1u, llvm::Attribute::NoCapture);

-  You may need to declare global constants in your module. The method
   for integers is similar to strings, but we show strings here because
   you will need it for use with ``printf``. For example, if I wanted to
   create a ``printf`` format string for integers (``module`` is
   ``llvm::Module`` and ``context`` is ``llvm::Context``):

   ::

            #include "llvm/IR/Constant.h"
            #include "llvm/IR/GlobalVariable.h"
            #include "llvm/Support/Cast.h"
            ...
            // Create the constant data array of characters.
            llvm::Constant *intFormatStr = llvm::ConstantDataArray::getString(context, "%d");

            // Create the global space we will use. The string "intFormatStr" is the name you will need to
            // to use to ask for this value later to get it from the module.
            auto *intFormatStrLoc =
              llvm::cast<llvm::GlobalVariable>(
                module.getOrInsertGlobal("intFormatStr", intFormatStr->getType())
              );

            // Set the location to be initialised by the constant.
            intFormatStrLoc->setInitializer(intFormatStr);

-  Calling functions is roughly the same in all places, but ``printf``
   can be a little annoying to begin with because of the way it is
   defined, so here is some more boilerplate code for calling that as
   well (``module`` is ``llvm::Module``):

   ::

            #include "llvm/IR/Function.h"
            #include "llvm/Support/Cast.h"
            ...
            // Note that we use getFunction not getOrInsertFunction. This will blow up if you haven't
            // previously defined printf in your module. See above.
            llvm::Function *printfFunc = module.getFunction("printf");

            // Get your string to print.
            auto *formatStrGlobal = llvm::cast<llvm::Value>(mod.getGlobalVariable("my string name"));

            // The type of your string will be [n x i8], it needs to be i8*, so we cast here. We
            // explicitly use the type of printf's first arg to guarantee we are always right.
            llvm::Value *formatStr =
              ir.CreatePointerCast(formatStrGlobal, printfFunc->arg_begin()->getType(), "formatStr");

            // Get our value.
            llvm::Value *value = <appropriate code to get your value to print>;

            // Call printf. Printing multiple values is easy: just add to the {}.
            ir.CreateCall(printfF, {formatStr, value});

-  In case you wanted calloc (or malloc) as well:

   ::

              #include "llvm/IR/Attributes.h"
              #include "llvm/IR/DerivedTypes.h"
              #include "llvm/IR/Function.h"
              #include "llvm/IR/TypeBuilder.h"
              #include "llvm/Support/Cast.h"
              ...
              // Declare calloc. Returns char *, takes array size, element size.
              llvm::FunctionType *fTy = llvm::TypeBuilder<char *(size_t, size_t), false>::get(ctx);
              auto *callocFunc = llvm::cast<llvm::Function>(mod.getOrInsertFunction("calloc", fTy));

              // Add the suggested function attributes.
              callocFunc->addFnAttr(llvm::Attribute::NoUnwind);
              callocFunc->addAttribute(0, llvm::Attribute::NoAlias);

