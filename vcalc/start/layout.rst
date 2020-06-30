Project Layout
--------------

For the tools provided to work your project should be in the specified
layout.

::

     +-- cmake
     |   +-- antlr_generate.cmake
     |   +-- get_antlr.cmake
     |   +-- get_antlr_manual.cmake
     |   +-- get_llvm.cmake
     |   +-- symlink_to_bin.cmake
     +-- CMakeLists.txt
     +-- grammar
     |   +-- VCalc.g4
     +-- include
     |   +-- placeholder.h
     +-- LICENSE.md
     +-- README.md
     +-- scripts
     |   +-- configureLLVM.sh
     +-- src
     |   +-- CMakeLists.txt
     |   +-- main.cpp
     +-- tests
         +-- input
         |   +-- ...
         +-- output
             +-- ...
         +-- VCalcConfig.json

