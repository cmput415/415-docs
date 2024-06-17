Tips and Hints
==============

#. The learning curve for *LLVM* and *MLIR* is not trivial: **START EARLY**.
   There will be a lot of things to learn. If you can’t figure out how
   to do something don’t be afraid to ask. Someone else will know or
   someone else will also want to know.

   As well, you should check the *MLIR/LLVM* Tips and Hints section for a
   good starting place.

#. You should definitely consider making an AST in this assignment.
   While it’s not strictly necessary it can be a great help, and you’ll
   be much better equipped moving into *Gazprea*.

   You should check the AST Tips and Hints section for a good starting
   place here as well.

#. Write tests **BEFORE** you implement the things they will test.

#. Reuse your tests from *SCalc*.

#. There are times when you do not want to visit the tree in order (e.g.
   filters/generators), this makes using a listener difficult. We
   suggest using a visitor.

#. Try to plan ahead of time to avoid having to rewrite things.
   Occasionally you will need to rewrite portions of your code if you
   find a new complication. You can mitigate some of this with modular
   design.

#. Your files in this project can get quite large. Don’t be afraid to
   split them up. Remember that you can have multiple implementation
   files per header file but you should still try to keep similar things
   together.

#. Remember that your style should be consistent. Now that you’re in a
   team you should discuss some probable points of code contention to
   make sure you’re on the same page.

#. This is the biggest assignment, thus **START EARLY**. **DO NOT USE
   LLVM IR VECTOR TYPES**. These types are designed for Single
   Instruction Multiple Data (SIMD) processing. They are also
   architecture specific on implementation. Using the LLVM IR vector
   types will result in a segmentation fault in architectures that do
   not support them. Not all lab machines support the *LLVM IR* vector.

#. The `Getting Started with the LLVM System <https://llvm.org/docs/GettingStarted.html>`__
   can help introduce you to *LLVM*. For *MLIR*, see `Getting Started <https://mlir.llvm.org/getting_started>`__.
   In particular, sections three and five of the `Kaleidoscope tutorial <https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/index.html>`__ are of particular interest for generating *LLVM IR*. Generating *MLIR* is similar.
   Section 7 is worth looking through for more discussion of the use of
   ``alloca`` over ``phi`` nodes.
   The other sections can be read at your own discrection.

#. The demo that was presented in the lab can be found
   `here <../_static/labdemo.tar.gz>`__.
   Remember to set it up in CLion just like you did with your regular
   project (environment variables).

