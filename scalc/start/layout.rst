Project Layout
--------------

For the tools provided to work your project should be in the specified
layout.

.. code-block:: text

    .
    ├── cmake
    │   ├── antlr_generate.cmake
    │   ├── get_antlr.cmake
    │   └── symlink_to_bin.cmake
    ├── CMakeLists.txt
    ├── grammar
    │   └── SCalc.g4
    ├── include
    │   ├── inja.hpp
    │   └── nlohmann
    │       └── json.hpp
    ├── LICENSE.md
    ├── README.md
    ├── src
    │   ├── CMakeLists.txt
    │   └── main.cpp
    └── tests
        ├── SCalcConfigCS.json
        ├── SCalcConfigInterpreterOnly.json
        └── testfiles