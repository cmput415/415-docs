Tips and Hints
==============

-  Write tests *before* you implement the things they will test. The
   testing script provided is designed to handle failed test cases. You
   can reduce output in the testing tool by passing the ``-q`` flag.

-  Make sure you’ve *read the documentation for ANTLR4*. Here is the
   link again `Antlr4
   documentation <https://github.com/antlr/antlr4/blob/master/doc/index.md>`__.

-  *Antlr4* has two ways of navigating the parse tree, visitors and
   listeners. For this assignment, visitors can prove more effective.

-  Be careful with your lexer rule ordering. Remember that the lexer
   matches tokens according to definition order and not according to any
   parser rules.

-  In particular, *rule element labels* can be supremely useful. More
   info can be found
   `here <https://github.com/antlr/antlr4/blob/master/doc/parser-rules.md#alternative-labels>`__.

-  Style and design are part of your mark. Here are some easy ways to
   ensure you remain stylish:

   -  *ANTLR4* has no standardized naming convention or style guide.
      This means you *could* do whatever you want for style. With that
      in mind I highly recommend you follow something similar to the one
      on the *ANTLR4* documentation pages. What ever you choose make
      sure it is easy to read and consistent.

   -  Keep your source organised. That means separating declarations
      (classes, class member functions, file scope functions) into
      headers and their definitions into source files. A good rule of
      thumb: if you’re writing three or more lines of function code in a
      header, it’s probably better in a source file. There are of course
      exceptions (template classes/functions, etc.) but their
      definitions can often be separated to below the class declaration
      to keep a "clean" declaration. If you can’t follow this style for
      some reason, leave a comment for yourself (and the marker) to
      understand why. Consider reading `this
      answer <https://softwareengineering.stackexchange.com/a/167751>`__
      for more info.

   -  Now that you’ve separated all of these files, you should make sure
      they’re organised. The project is already set up to let you
      separate your headers from your source. A good idea is to have
      identical directory structures under ``src`` and ``include`` with
      headers and source files mirroring each other (e.g.
      ``include/dir/dir2/class.h`` and ``src/dir/dir2/class.cpp``). You
      will be able to include the header via
      ``#include "dir/dir2/class.h"``.

   -  This is your work and you should own that. Add your name to the
      README and License as well. Your project is not "GeneratorBase".
      Change the base ``CMakeLists.txt``\ ’s project name to something
      more appropriate. "Generator", "<ccid>Generator" or something
      equally descriptive should be more appropriate. Just don’t change
      the executable name!

   -  You will also need to add your source files in the
      src/CMakeLists.txt file (or new subdirectory ``CMakeLists.txt``\ s
      that you make yourself). You should be explicit about your file
      paths (use ``CMAKE_CURRENT_SOURCE_DIR`` to make them absolute).
      `These
      variables <https://cmake.org/Wiki/CMake_Useful_Variables>`__ may
      be helpful.

   -  This assignment is not as demanding as later assignments so a lack
      of documentation and information might be understandable. However,
      in the future, I expect to see appropriate comments in source and
      headers, changes to README where applicable, using the issue
      tracker, etc.

-  The ``antlrcpp::Any`` type returned by ``visit`` can be very fickle
   if you don’t understand its internals exactly (`if you’re
   curious <https://github.com/antlr/antlr4/blob/master/runtime/Cpp/runtime/src/support/Any.h>`__).
   Instead of spending hours in that file, consider these best
   practices:

   -  Ensure the type you’re returning is what you want to receive. You
      may *think* you’re returning a certain type, but unless there is
      an explicit cast in the return statement or you’re returning a
      typed variable you may get inexpicable type errors from ``Any``.
      In other words, don’t return temporaries. For example, this will
      break if the receiving side wants a pointer to the parent class
      even though there’s an available typesafe cast:

      ::

                   {
                     ...
                     return std::make_shared<MyChildClass>(...);
                   }

   -  Ensure the type you’re receiving from a call to ``visit`` is what
      you expected. The problem is a two way street. See the above
      reasons.

   These may not seem relevant now, but it’s better to get in the habit
   now than have it bite you later and not understand why.
