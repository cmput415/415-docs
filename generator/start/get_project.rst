Getting Your Project
====================

We will be using GitHub to manage our assignments.

#. Follow the assignment link on eclass to receive your repository.

#. Clone your repository to your working directory.

   ::

            git clone <repository_clone_link>

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
   |   +-- Generator.g4
   +-- include
   |   +-- placeholder.h
   +-- LICENSE.md
   +-- README.md
   +-- src
       +-- CMakeLists.txt
       +-- main.cpp
   +-- tests
       +-- GeneratorConfig.json
       +-- input
           +-- ...
       +-- output
           +-- ...

