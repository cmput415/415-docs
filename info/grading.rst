Grading
=======

Your assignment grades will be computed based on the following matrix:

.. _sec:grading_matrix:


Grading Matrix
--------------

The following table shows the weight distribution for each grading category across different assignments in *CMPUT 415*.

+------------------------+-----------+---------+---------+--------------+--------------+
| **Grading Category**   | Generator | SCalc   | VCalc   |  Gazprea P1  |  Gazprea P2  |
+========================+===========+=========+=========+==============+==============+
| Code Style             | 15%       | 15%     | 15%     | 10%          | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Software Engineering   | 0%        | 0%      | 0%      | 5%           | 5%           |
+------------------------+-----------+---------+---------+--------------+--------------+
| Grammar                | 15%       | 5%      | 5%      | 5%           | 5%           |
+------------------------+-----------+---------+---------+--------------+--------------+
| Implementation         | 0%        | 10%     | 10%     | 10%          | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| TA Specification Tests | 50%       | 50%     | 50%     | 50%          | 40%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Competitive Testing    | 20%       | 20%     | 20%     | 20%          | 20%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Performance Testing    | 0%        | 0%      | 0%      | 0%           | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+


Code Style and Consistency
---------------------------------------------------
* You should have a consistent style throughout your assignment. For example: commenting, variable names,
  function names, class names, file names, indentation, etc… should be consistent in your program. You can
  use tools like clang-format and clang-tidy to support a consistent style. When working in teams for VCalc
  and Gazprea, you should discuss style early.
* You are expected to separate class definitions from implementations using header (.h) and source (.cpp)
  files.
* Your code should be clean and readable.
* There is no minimum expectation for commenting or documentation.

Software Engineering Process (Gazprea only)
---------------------------------------------------

* Each team should outline a software engineering process which they are expected to adhere to. This plan should be comprehensive. For example, a comprehensive plan would specify commit conventions, branch structure, code style conventions, CI jobs to be used, etc.

* Each team should be ready to present evidence that they adhered to their plan. It is suggested to create
a PLAN.md (or similarly named) file in the base of your repo. Updating your plan throughout the project is fine so long as it represents an improvement to the process.

* Failure to specify a thorough plan or to adhere to it may result in mark deductions from this category.
Otherwise, this should be an easy 5%. The most successful teams will establish a clear software engineering process even without being explicitly required.

Grammar
---------------------------------------------------
* Your grammar should correctly implement the specification.
* Your grammar should have a consistent style.
* Your grammar should be clean and readable.

Implementation Guidelines Compliance
---------------------------------------------------
* You should comply with the implementation guidelines described for the assignments.

  * **Generator:**
    N/A

  * **SCalc:**

    * You should comply with the guidelines described
      `here <https://cmput415.github.io/415-docs/scalc/index.html>`_.

  * **VCalc:**

    * You should write your compiler as a series of passes each with simple functionality. Do not implement
      your compiler as a single pass. As a minimum, your compiler should individual passes that perform
      each of the following actions:

      * Create an abstract syntax tree.
      * Emit LLVM, SCF, Memref and Arith Dialects that can be lowered into LLVM IR.

  * **Gazprea:**

    * You should write your compiler as a series of passes each with simple functionality. Do not implement
      your compiler as a single pass. As a minimum, your compiler should individual passes that perform
      each of the following actions:

      * Create an abstract syntax tree.
      * Define symbols and ensure that symbols can be referenced in the locations they are used. These
        actions may be performed by two separate passes.
      * Propagate type information through expressions and perform static type checking. These actions may
        be performed by two separate passes.
      * Emit LLVM, SCF, Memref and Arith Dialects that can be lowered into LLVM IR.

    * Your compiler should use a symbol table to track symbol definitions and scopes.

TA Specification Tests
---------------------------------------------------

* For each assignment, your submission will be tested on a private test-suite that tests the features
  defined in the assignment specification.

Competitive Testing
---------------------------------------------------

* Competitive testing rules are outlined here: :doc:`testing`.

Performance Testing
---------------------------------------------------

* The speed of the executable your compiler produces will be put to the test against all other compilers.
  See here :doc:`testing` for details.


After each submission of a team assignment you must fill out a
team assessment. Reach out to the TA if your team encounters problems with collaboration that you are
unable to resolve on your own. Your final individual grade may be lower than your team grade by a factor
proportional to your contribution to the assignment.

.. note::
   © 2024 University of Alberta. All rights reserved.
