.. _sec:lab_exam_vehicles:

Exam Vehicles
=============

:doc:`Lab Exams <lab_exam>` describes the format every lab exam shares. This page describes the codebases the exams are written in — what a "vehicle" is, why each one is a language you have not seen before, and what carries over from one exam to the next.

What a vehicle is
------------------

Each lab exam gives you a **small, complete, working program in a language you have not seen before**, built out of the same parts as the project it follows: the same kind of front end, the same toolchain, the same test format. That program is the exam's *vehicle* — it is what you read, debug, test, and extend during the hour.

A vehicle is never your own submission or your teammates'. The project is graded on a working compiler, and nobody can tell from a repository alone which member of a team understood which part of it. Because the vehicle is unfamiliar, you cannot fall back on code you happen to remember writing, and a team whose work was unevenly divided does not get to hide that in the exam.

Everything you need in order to work out what a vehicle *should* do is in its repository — most importantly ``SPEC.md``, which every vehicle carries. The spec defines correct behaviour, and it is what you check the implementation against. Read it first; every exam task is stated relative to the spec.

The four vehicles
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Exam
     - Vehicle
     - What it exercises
   * - Generator
     - *Sweep*
     - A tiny ``sweep``/``yield`` expression language, parsed and interpreted with ANTLR4 and C++. No MLIR, no LLVM — the same shape as the Generator project's own front end.
   * - LOLCODE
     - *littleC*
     - A small C-like language, parsed by a hand-written recursive-descent parser over an ANTLR4-generated token stream, then walked directly by a tree-walking interpreter. No code generation, matching the LOLCODE project's own parser-plus-interpreter structure.
   * - VCalc
     - *littleC*
     - A more complex C-like language, compiled to LLVM IR through MLIR, the same backend path the VCalc project builds. Every operator applies elementwise to arrays, the way VCalc's own vector operators do.
   * - Gazprea
     - *littleC*
     - A still more complex littleC, again compiling to LLVM IR through MLIR.

Three of the four exams use a language called **littleC**, each its own separate, self-contained codebase with its own repository, its own spec, and its own tasks. C is chosen because its syntax is already familiar by the time you reach these exams — you have read and written it since Generator — so these three exams test you on semantics rather than syntax. Each littleC's semantics mirror the project it follows as closely as a small C-like language allows: VCalc's littleC applies operators elementwise to arrays, and Gazprea's adds functions, the way those projects' own languages do.

Despite the shared name, the three littleCs are not strict subsets of each other, or of C. Each is a separate language with its own spec, and features present in one are not guaranteed to appear, or to mean the same thing, in the next. Passing familiarity with one littleC does not substitute for reading the next one's spec.

What stays the same across every vehicle
-----------------------------------------

Whatever the language, every vehicle's repository is laid out the same way:

* ``SPEC.md``, the **language spec**, defining correct behaviour and how to build and run the program.
* ``EXAM.md``, holding the exam's tasks and their point values.
* ``tests/``, holding the test configuration and an empty directory for the tests you write. No reference tests ship with it — writing the tests that expose the behaviour you are looking for is part of the exam.
* ``ANSWERS.md``, where a vehicle's exam asks for a written answer alongside code.

Every vehicle builds and tests the way the project it follows does: the same CMake/ANTLR4 setup, the same ``dragon-runner`` invocation for running tests. If you can configure, build, and test the project you just submitted, you already know the commands the exam needs — only the source tree under them is new.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
