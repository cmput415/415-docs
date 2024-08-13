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

MLIR Dialect tips
-----------------

You and your team member(s) will face an important decision regarding which dialects to use and to
what extent. The four dialects ``llvm``, ``scf``, ``memref`` and ``arith`` exist at various
"heights" in the MLIR tree; interactions between types and operations in each dialect can be
surprising. This page lays out some of the common pitfalls to watch out for.

SCF Ops and Regular LLVM Control Flow 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``scf`` Ops such as ``scf.if``, ``scf.for`` and ``scf.while`` offer convenient, modular interfaces
for creating control flow that abstract away much of the minute detail of manually laying out basic
blocks. In contrast, the ``llvm`` dialect offers fine-grained control over how basic blocks are laid
out in your program. 

If both ``llvm`` and ``scf`` sound tempting, there is one unfortunate caveat: **All scf ops only
allow one basic block in their body**. As a consequence, ``scf`` ops cannot be mixed with ``llvm``
control flow. Under this restriction, for example, nesting an ``llvm`` while loop made with basic
blocks inside an ``scf.if`` Op is impossible. This imposes that control flow be implemented "all or
nothing" with either ``scf`` or ``llvm``. (By control flow here we mean only the
``intra-procedural`` kind -- excluding functions which are always implemented in the ``llvm``
dialect)

Large, Composite Memref Types & the C Runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will find a C runtime library ready to go in both ``vcalc`` and ``gazprea``. This library
allows interoperability with the ``llvm`` dialect you emit. Teams often find the runtime convenient
for printing vectors and matrices as well as for I/O operations.

One challenge with the runtime comes if choosing to implement vectors using the ``memref`` dialect.
With each ``memref.alloc`` or ``memref.alloca`` op, various metadata is stored such as the
dimensions, alignment, and element type. As a consequence, the corresponding ``C`` type needed to
"catch" a memref value on the receiving side of a function call is a large struct.

In contrast, a vector implemented with ``alloca`` or a ``malloc`` can be passed to the runtime as a
``void *`` C type or ``llvm.i8*`` ``llvm`` type.