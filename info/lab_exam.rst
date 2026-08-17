.. _sec:lab_exam:

Lab Exams
=========

Each project is followed by a lab exam: an individual, written-in-person assessment of whether you can work in a compiler codebase yourself. There are four, one per project — Generator, LOLCODE, VCalc, and Gazprea.

The exam is a programming exercise, not a written test. You are given a small codebase, and you fix a bug in it, write a test for it, and add a feature to it, on a lab machine, in the same development environment you use for the projects.

The projects are graded on a working compiler; nobody can tell from a repository which member of a team understood what. The lab exam is where you show that individually.

Schedule
--------

Each exam runs in a lab section, held synchronously — everyone writes at the same time. You are given 80 minutes at the keyboard.

An exam takes place after its project's deadline, so the material is fresh and nothing in the exam gives away a project you have not submitted.

Where the exam runs
-------------------

Exams are written **in person, on the lab machines**. Sign in at any machine in the room with your CCID.

The environment is the one you already use for the projects. If you have followed the `CS computers setup <../setup/cs_computers.html>`_, the toolchain — a compiler, CMake, Java, ANTLR, and ``dragon-runner`` — is already on the path. You do not need to install anything on exam day.

You may use whichever editor and tools you normally develop with, as long as they are already on the lab machines. Set up and test that choice before exam day, not during the exam.

What you are given
------------------

At the start of the exam you are given a link to a GitHub template repository. You instantiate it into your own repository, clone it, and work there.

The codebase is a **small, complete, working program in a language you have not seen before** — but one built out of the same parts as the project it follows. The Generator exam, for example, uses *Sweep*, a tiny ``sweep``/``yield`` interpreter written with ANTLR 4 and C++. It is not your own submission and not your teammates'.

This is deliberate. You cannot fall back on code you happen to remember writing, and a team whose work was unevenly divided does not get to hide that. Everything you need in order to work out what the program *should* do is in the repository:

* ``README.md`` specifies the language: its syntax, its operators, their precedence and associativity, and how to build and run it. This is the definition of correct behaviour, and it is what you check the implementation against.
* ``EXAM.md`` contains the exam tasks and their point values.
* ``tests/`` holds the test configuration and an empty directory for the tests you write. **No reference tests are shipped** — writing the tests that expose the behaviour you are looking for is part of the exam.

Read ``README.md`` first. The tasks are all stated relative to it.

What you will be asked to do
----------------------------

The tasks fall into three kinds, and one exam contains all three:

**1. Fix a bug.** The implementation does not match the behaviour ``README.md`` specifies somewhere. You are not told where. Find it — writing tests is how — and fix it.

**2. Write a test.** You are asked for a test that distinguishes one specific behaviour from a plausible wrong one: it must pass when the implementation is correct and fail when it is not. Naming a behaviour is not enough; the test has to separate the two cases.

**3. Add a feature.** A language feature described in ``README.md`` is missing from the implementation. Implement it so that it behaves as specified, including where it interacts with features that are already there.

The three tasks are independent. Each can be done and verified without any of the others being finished, so a task you cannot get working does not cost you the ones you can.

You do not have to do them in order.

Grading weighs **understanding over syntax**. Code that clearly demonstrates the right idea but does not compile is worth more than nothing, and a fix that happens to pass while showing no grasp of the problem is worth less than full marks. Working, tested code is still the target — this is a statement about partial credit, not permission to hand in something that does not build.

Internet access and reference material
--------------------------------------

**The exam is closed-internet.** General web browsing, search engines, and AI assistants of any kind are not permitted.

Reference documentation is provided **locally on the lab machines** instead — the C++ standard library, ANTLR, and the LLVM and MLIR headers, depending on the project. You are expected to use it. The exam does not test whether you have memorised an API.

You may consult the local documentation and anything in the exam repository. That is the whole list.

Monitoring
----------

At the start of the exam you run a monitoring script in a terminal and leave it running until you are finished. It clones the exam repository for you and records activity on the machine for the duration of the exam, including network lookups.

You will be shown the script and told exactly what it records at the dry run, before the exam. Leaving it running is a requirement of writing the exam.

Submitting your work
--------------------

**You are graded on your last pushed commit before the deadline.** Not your working tree, not your local commits.

Push early and push often. A commit sitting unpushed on a lab machine at the end of the exam is not a submission, and "it was finished locally" is not something anyone can verify afterwards.

Committing each task as you finish it is recommended but not required — you will not lose marks for one commit at the end, only for one commit that never left the machine.

Before the exam: the dry run
----------------------------

A dry run is held ahead of the first exam so you can confirm your setup works on a lab machine. Treat it as mandatory even if it is not.

Use it to check that:

* You can sign in at a lab machine and reach your GitHub account from it.
* Your editor of choice starts and works there.
* You can clone, configure, build, and run a project from scratch on that machine.
* You can run ``dragon-runner`` against a test file.
* The monitoring script runs on your session.

An environment problem discovered at the dry run is a minor inconvenience. The same problem discovered at the start of the exam costs you exam time, and the clock does not stop for it.

If something goes wrong
-----------------------

Machine and network failures happen. If yours fails during the exam, tell an invigilator immediately rather than trying to recover on your own — how much time you lose depends on how quickly it is reported.

A **paper version of every lab exam** is prepared as a fallback. If the lab machines or the network are unavailable, the exam still runs, on paper, covering the same material.

Preparing
---------

Nothing about the exam rewards memorisation, and there is no set of notes that substitutes for having done the work. What helps:

* **Do your share of the project.** The exam asks for the same skills the project asks for, on a codebase you have never seen. There is no shortcut around having practised them.
* **Practise reading unfamiliar code.** Getting oriented in a codebase you did not write — finding where a construct is handled and following it through — is the first thing you do in the exam and the thing time pressure punishes most.
* **Practise debugging from a failing test.** Given wrong output, be able to work backwards to which part of the implementation produced it.
* **Be fluent with the tools.** Configuring a build, rebuilding after an edit, and running the test suite should be automatic. Fumbling the build costs exam time that is not coming back.
* **Know your language specification.** A precise account of precedence, associativity, and evaluation order is what lets you tell a bug from intended behaviour.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
