Grading
=======

Programming assignments are assessed from three different perspectives:
written artefects or deliverables, a lab quiz, and a peer evaluation.
This section describes each grading element so that you and your team can
prepare as needed. The weighting of each grading perspective is as follows:


+-------------------+-----------+---------+--------+--------------+--------------+
| **Perspective**   | Generator | LOLCODE | VCalc  |  Gazprea P1  |  Gazprea P2  |
+===================+===========+=========+========+==============+==============+
| Written Artefacts | 40%       | 50%     | 60%    | 34%          | 50%          |
+-------------------+-----------+---------+--------+--------------+--------------+
| Lab Quiz          | 60%       | 50%     | 40%    | 33%          | 0%           |
+-------------------+-----------+---------+--------+--------------+--------------+
| Peer Evaluation   | 0%        | 0%      | 0%     | 33%          | 50%          |
+-------------------+-----------+---------+--------+--------------+--------------+


Written Artefacts
------------------

A successful product or project is the culmination of many small parts that
work together. No one part can take all the credit for a success, they must
all be present and executed correctly. While different projects emphasize and
identify different criterion, we will focus on the following: design, project
management, grammar, implementation, completeness, correctness, and performance.

Design
------

Your design write-up should describe the top-level architecture, which usually
comprises the major components within your product, their responsibilities, and
the general flow of information between them. The design document should also
identify and describe key data structures/algorithms and why you chose them.

Remember that functional correctness is only a small part of the design.
A good design (and implementation) addresses the important aspects of a
product: scalability, flexibility, and maintainability.

  * **LOLCODE** There are likely only two components: the parser and the
    interpreter, but there are a number of key design decisions, for example
    the token/grammar structure and the design of the AST nodes.
    The interpreter must be an external walker, and must handle symbols and
    control flow.

  * **VCalc** The information flow in this project is much more interesting.
    You need to design an AST and Symbol table, and use them to implement
    multiple passes including: symbol definitions, symbol resolutions and
    semantic checking, type checking, and code generation.

  * **Gazprea** While the top-level architecture is almost identical to
    *VCalc*, the rich type system within can increase complexity
    substantially unless it is managed. It is also important to understand
    and select dialects that make sense for your design.

Software Engineering Processes
------------------------------

Project management practices come into play on large projects where multiple
developers or teams are working simultaneously on different parts of the project.
The design must be decomposed into tasks and each task must be sized and
assigned such that each team member has an equal amount of (estimated) work.
It can help to break large tasks into smaller sub-tasks, because sizing can be
more accurate, but dependencies between sub-tasks must be identified so that a
critical path can be identified.

Record the tasks you identify as issues, and assign each one to the member doing it. Agree on the rest of the development process early: commit conventions, how a change reaches the default branch, and who reviews it before it does. A typical process is that each feature pull request carries the tests that demonstrate its correctness.

It is important to actually track the tasks that you identified. Often you will
have to refine/resize them or discover new tasks that must be sized and
assigned. Only by tracking these tasks can you know that your team can deliver
your product on time.

.. _sec:gazprea_pm_marks:

Gazprea project management marks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Four marks at Part 1 and four at Part 2, awarded to the team. Setting up the process these are read from is described under :external+gazprea:doc:`Project Management <impl/process>`.

.. list-table::
   :header-rows: 1
   :widths: 12 88

   * - Marks
     - Line
   * - 1
     - **Delivery by pull request.** At least four pull requests merged into the default branch during the part.
   * - 2
     - **Review before merge.** The fraction of those merged pull requests that a non-author teammate approved before they were merged.
   * - 1
     - **Work tracked in issues.** At least two issues opened during the part and assigned to a member.

Counts are taken over the part being marked, so Part 2 starts from zero rather than carrying Part 1 forward.


Grammar
-------
* Your grammar should correctly implement the specification.
* Your grammar should have a consistent style.
* Your grammar should be clean and readable.


Implementation Guidelines Compliance
---------------------------------------------------

Your implementation should comply with the guidelines provided in the
assignment's specification.

In general, your implementation should demonstrate object-oriented design
principles: information hiding, abstraction, encapsulation and hierarchical
specialization. Your file structure and layout should be intuitive and
consistent. Note that good file structure (and communication!) can dramatically
reduce merge-conflicts and all the time they waste.

You should be using Test Driven Development principles although for compilers
the tests are typically at the feature level vs the unit level. You should also
be testing or verifying that your porgram does not leak or stomp memory.
Remember that most products are only as good as their tests!

Code Style and Consistency
^^^^^^^^^^^^^^^^^^^^^^^^^^
* You should have a consistent style throughout your assignment. For example: commenting, variable names,
  function names, class names, file names, indentation, etc… should be consistent in your program. You can
  use tools like clang-format and clang-tidy to support a consistent style. When working in teams for VCalc
  and Gazprea, you should discuss style early.
* You are expected to separate class definitions from implementations using header (.h) and source (.cpp)
  files.
* Your code should be clean and readable.
* There is no minimum expectation for commenting or documentation.

TA Specification Tests
----------------------

For each assignment, your submission will be tested on a private test-suite
that tests the features defined in the assignment specification.

Competitive Testing
-------------------

Competitive testing rules are outlined here: :doc:`testing`.

Coherence Testing
-----------------

Coherence testing was first introduce to check that the tests submitted for
competitive testing could be compiled by the team that submitted them.
We can extend this concept to other introspective tests, for example `valgrind`
is very good at checking if a program leaks memory. Even the time it takes to
compile a set of benchmark programs can reveal much about the internal structure
of a compiler.

Performance Testing
-------------------

Performance testing attempts to measure the speed of the executable your
compiler produces. While your compiler will not do direct optimizations itself,
it can still produce intermediate code that is amenable to optimization.

.. _sec:grading_matrix:


Grading Matrix
--------------

The following table shows the weight distribution for each grading category across different assignments in *CMPUT 415*.

+------------------------+-----------+---------+---------+--------------+--------------+
| **Grading Category**   | Generator | LOLCODE | VCalc   |  Gazprea P1  |  Gazprea P2  |
+========================+===========+=========+=========+==============+==============+
| Design                 | 5%        | 15%     | 15%     | 15%          | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Software Engineering   | 0%        | 0%      | 5%      | 5%           | 5%           |
+------------------------+-----------+---------+---------+--------------+--------------+
| Grammar                | 25%       | 15%     | 5%      | 5%           | 5%           |
+------------------------+-----------+---------+---------+--------------+--------------+
| Implementation         | 0%        | 15%     | 10%     | 10%          | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| TA Specification Tests | 50%       | 35%     | 35%     | 50%          | 40%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Competitive Testing    | 20%       | 20%     | 20%     | 0%           | 20%          |
+------------------------+-----------+---------+---------+--------------+--------------+
| Coherence Testing      | 0%        | 0%      | 5%      | 5%           | 0%           |
+------------------------+-----------+---------+---------+--------------+--------------+
| Performance Testing    | 0%        | 0%      | 5%      | 10%          | 10%          |
+------------------------+-----------+---------+---------+--------------+--------------+

After each submission of a team assignment you must fill out a
team assessment. Reach out to the TA if your team encounters problems with collaboration that you are
unable to resolve on your own. Your final individual grade may be lower than your team grade by a factor
proportional to your contribution to the assignment.

Late Policy
---------------------------------------------------
At the moment of the deadline repositories are automatically pulled from Github Classroom. In the case
of a late submission, the following policy is employed.

* Late submissions within the first 24 hour interval after the deadline are excluded from the competitive testing tournament.
* If competitive testing is not being organized for this assignment for any reason, a commensurate deduction will be applied.
* Each 24 hour interval thereafter a 10% deduction is incurred.
* Marks for submissions late beyond three days are capped at the minimum passing grade.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
