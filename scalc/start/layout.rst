Project Layout
--------------

For the tools provided to work your project should be in the specified
layout.

::

     +-- cmake
     |   +-- antlr_generate.cmake
     |   +-- get_antlr.cmake
     |   +-- get_antlr_manual.cmake
     |   +-- symlink_to_bin.cmake
     +-- CMakeLists.txt
     +-- grammar
     |   +-- SCalc.g4
     +-- include
     |   +-- inja.hpp
     |   +-- nlohmann
     |   |   +-- json.hpp
     |   +-- placeholder.h
     +-- LICENSE.md
     +-- README.md
     +-- src
         +-- CMakeLists.txt
         +-- main.cpp
     +-- tests
         +
         +-- input
             +-- ...
         +-- output
         |   +-- ...
         +-- SCalcConfigCS.json
         +-- SCalcConfigInterpreterOnly.json

