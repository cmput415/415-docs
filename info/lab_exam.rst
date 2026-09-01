.. _sec:lab_exam:

Lab Exams
=========

Each project is followed by a lab exam: an individual, written-in-person assessment of whether you can work in a compiler codebase yourself. The exact set of exams and the weight each carries in your grade are announced with the course outline.

The exam is a programming exercise. You are given a small codebase, and you fix a bug in it, write a test for it, and add a feature to it, on a lab machine, in the same development environment you use for the projects.

The projects are graded on a working compiler; nobody can tell from a repository which member of a team understood what. The lab exam is where you show that individually.

What to bring
-------------

* Your **OneCard**. A proctor checks it against your session at the start of the exam.
* Your CCID and your GitHub credentials, both confirmed working on a lab machine at the dry run.
* Any notes or cheat sheet you want to work from, already saved somewhere on the lab filesystem.

Phones and other personal devices are put away for the duration of the exam.

Schedule
--------

Exams are written during the Friday lab section, in the week following the deadline of the project they cover, while the material is fresh.

The exam is synchronous — everyone writes at the same time. The tasks are set to be finished in one hour, and **every student is given two and a half hours at the keyboard**: the course applies the University's `universal time multiplier <https://www.ualberta.ca/en/centre-for-teaching-and-learning/resources/access-community-belonging/access-and-accessibility/universal-time-multipliers.html>`_ of 2.5× to the whole class.

The lab block runs 2:00 to 4:50 PM. Sign-in and setup happen at the start of the block, before the clock starts.

Where the exam runs
-------------------

Exams are written **in person, in the CMPUT 415 lab rooms** — UCOMM 2-086 and 2-070, with the class split across the two. Sign in at any machine in your assigned room with your CCID.

You must be physically at the lab machine. The exam cannot be written over SSH.

The environment is the one you already use for the projects. If you have followed the :external+setup:doc:`CS computers setup <cs_computers>`, the toolchain — a compiler, CMake, Java, ANTLR, and ``dragon-runner`` — is already on the path, and your ``/cshome`` directory is the same one you see from any other CS machine. You do not need to install anything on exam day.

You may use whichever editor and tools you normally develop with, as long as they are already on the lab machines. Set up and test that choice before exam day.

What you are given
------------------

The exam is distributed through Classroom 50, the same way project repositories are. Accepting the assignment creates a private repository of your own from the exam template:

.. code-block:: console

   $ gh student accept <assignment>

Clone that repository onto the lab machine and work in it. You practise these exact steps at the dry run.

The codebase is a **small, complete, working program in a language you have not seen before**, built out of the same parts as the project it follows. :doc:`Exam Vehicles <lab_exam_vehicles>` names each exam's vehicle, what it exercises, and why the exams are written in an unfamiliar language.

Everything you need in order to work out what the program *should* do is in the repository:

* ``SPEC.md`` specifies the language: its syntax, its operators, their precedence and associativity, and how to build and run it. This is the definition of correct behaviour, and it is what you check the implementation against.
* ``EXAM.md`` contains the exam tasks and their point values.
* ``tests/`` holds the test configuration and an empty directory for the tests you write. **No reference tests are shipped** — writing the tests that expose the behaviour you are looking for is part of the exam.

Read ``SPEC.md`` first. The tasks are all stated relative to the spec.

What you will be asked to do
----------------------------

The tasks fall into four kinds:

**1. Fix a bug.** The implementation does not match the behaviour ``SPEC.md`` specifies somewhere. You are not told where. Find it by writing tests and fix it.

**2. Write a test.** You are asked for a test that distinguishes one specific behaviour from a plausible wrong one: it must pass when the implementation is correct and fail when it is not. 

**3. Add a feature.** A language feature described in ``SPEC.md`` is missing from the implementation. Implement it so that it behaves as specified, including where it interacts with features that are already there.

**4. Explain your work in writing.** A few sentences, in your own words, typed into ``ANSWERS.md``: what was broken, why your fix works, and which test exposes it. 

The coding tasks are independent. Each can be done and verified without any of the others being finished, so a task you cannot get working does not cost you the ones you can. You do not have to do them in order.

How it is graded
----------------

**Code is graded by building it on a lab machine and running it against a test suite you never see.** The suite is written to catch the mistakes each question is designed to expose. Pass all of it and the question is full marks.

**Code that does not build scores zero.** Nothing in the suite can run against a tree that does not compile. Push something that builds, even when it is incomplete: a partial feature earns whatever marks its tests pass.

**Test-writing questions are graded by running your test twice**, against a correct build of the language and against a broken one. Your test earns its marks by passing on the correct build and failing on the broken one.

What you may use
----------------

**The exam is closed-internet.** The one thing you may use the network for is git traffic to your own exam repository on GitHub — cloning it at the start and pushing to it as you work. Nothing else: no web browsing and no search engines. **AI assistants of any kind are prohibited**, whether a chat interface, an editor completion, or a command-line tool, and whether it calls a hosted model or runs on the lab machine itself. Every reference you need is on the lab machine, so come prepared to search it from the command line. Any other network use is an academic integrity violation and is treated as such.

Nothing at the machine or the firewall blocks the network. Compliance is monitored instead, as described below.

Because of that, **turn off anything that reaches the network on its own before the exam starts**. Editor telemetry, update checks, plugin sync, and language servers that fetch as you type all produce connections under your name, and a connection you did not intend still has to be explained. VS Code ships with telemetry on: set ``telemetry.telemetryLevel`` to ``off`` in your settings. If you are not sure what your editor does at startup, find out at the dry run — that is one of the things the dry run is for.

Reference documentation is provided **locally on the lab machines** — the C++ standard library, ANTLR, and the LLVM and MLIR headers, depending on the project. Work from it. The exam does not test whether you have memorised an API, so look things up freely.

**The exam is open-computer.** Everything on the lab machine is yours to use, including your own home directory and everything you have put in it. Notes, a cheat sheet, and your own project repository open in a split pane for reference are all legitimate. Prepare them in advance.

**Phones and other personal devices are put away** for the duration of the exam, under the proctors' direction.

Monitoring
----------

At the start of the exam you run the session monitor in a terminal and leave it running until you are finished:

.. code-block:: console

   $ exammon <exam>

It is already on your ``PATH`` if you have sourced ``415env.sh``.

Starting it is part of writing the exam. Leave it running for the whole session; stopping it is an academic integrity violation. At the identity check a proctor confirms that your monitor is registered to the machine you are sitting at and to your name, so bring your OneCard.

If it will not start, or you think it has stopped, tell a proctor rather than carrying on without it.

Submitting your work
--------------------

**You are graded on what has reached GitHub by the end of the exam.**

Push early and push often. Timestamps in a local repository **can be spoofed**, so only what has reached GitHub can be credited once time is called. Pushing regularly across the session also protects your work if the machine fails.

Commit and ``git push`` to your repository's default branch, the same way you would on a project.

Before the exam: the dry run
----------------------------

A dry run is held ahead of the first exam so you can confirm your setup works on a lab machine. Treat it as mandatory.

Use it to check that:

* You can sign in at a lab machine and reach your GitHub account from it.
* ``gh student accept`` works for you, and you can push to the repository it creates.
* Your editor of choice starts and works there.
* Your editor and tools make no outgoing network connections once they are running. Find anything that reaches the network on its own and turn it off here, not on exam day.
* You can clone, configure, build, and run a project from scratch on that machine.
* You can run ``dragon-runner`` against a test file.
* ``exammon`` starts and stays running on your session.

An environment problem found at the dry run is fixed on your own time; the same problem at the start of the exam runs down the clock, and the clock does not stop for it.

If something goes wrong
-----------------------

Machine and network failures happen. If yours fails during the exam, tell an invigilator immediately rather than trying to recover on your own. Your allotted time can be adjusted for lost time only when the failure is reported as it happens.

A **paper version of every lab exam** is prepared as a fallback. If the lab machines or the network are unavailable, the exam still runs, on paper, covering the same material.

Preparing
---------

What helps:

* **Do your share of the project.** The exam asks for the same skills the project asks for, on a codebase you have never seen.
* **Practise reading unfamiliar code.** Getting oriented in a codebase you did not write — finding where a construct is handled and following it through — is the first thing you do in the exam and the thing time pressure punishes most.
* **Practise debugging from a failing test.** Given wrong output, be able to work backwards to which part of the implementation produced it.
* **Know the commands.** Configuring a build, rebuilding after an edit, running ``dragon-runner``, committing and pushing — you should be typing these without stopping to think. Fumbling the build costs exam time.
* **Get comfortable searching from the command line.** The reference documentation on the lab machines is a tree of files, and ``grep`` or ``rg`` (ripgrep) is how you find anything in it quickly.
* **Write yourself a cheat sheet.** The exam is open-computer, so anything you prepare beforehand is available during it. The commands you always end up looking up, a worked example of a test file, the shape of a visitor method: put them somewhere on the lab filesystem you can open in seconds.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
