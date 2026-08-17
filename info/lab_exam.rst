.. _sec:lab_exam:

Lab Exams
=========

Each project is followed by a lab exam: an individual, written-in-person assessment of whether you can work in a compiler codebase yourself. The exact set of exams and the weight each carries in your grade are announced with the course outline.

The exam is a programming exercise, not a written test. You are given a small codebase, and you fix a bug in it, write a test for it, and add a feature to it, on a lab machine, in the same development environment you use for the projects.

The projects are graded on a working compiler; nobody can tell from a repository which member of a team understood what. The lab exam is where you show that individually.

Schedule
--------

Exams are written during the Friday lab section, in the week following the deadline of the project they cover. The material is fresh, and nothing in an exam gives away a project you have not yet submitted.

The exam is synchronous — everyone writes at the same time — and you are given one hour at the keyboard. The lab block runs 2:00 to 4:50 PM, so there is room around the hour to get everyone signed in and set up before the clock starts.

Students with an exam accommodation for extra time receive **2.5× the standard duration**, which is two and a half hours. That has to fit inside the lab block, so if this applies to you, arrange your start time in advance — starting late enough to run past the end of the block is not something that can be fixed on the day.

Where the exam runs
-------------------

Exams are written **in person, in the CMPUT 415 lab rooms** — UCOMM 2-086 and 2-070, with the class split across the two. Sign in at any machine in your assigned room with your CCID.

You must be physically at the lab machine. SSH access is how you work on the projects; it is not how you write the exam.

The environment is the one you already use for the projects. If you have followed the `CS computers setup <../setup/cs_computers.html>`_, the toolchain — a compiler, CMake, Java, ANTLR, and ``dragon-runner`` — is already on the path, and your ``/cshome`` directory is the same one you see from any other CS machine. You do not need to install anything on exam day.

You may use whichever editor and tools you normally develop with, as long as they are already on the lab machines. Set up and test that choice before exam day, not during the exam.

What you are given
------------------

The exam is distributed through Classroom 50, the same way project repositories are. Accepting the assignment creates a private repository of your own from the exam template:

.. code-block:: console

   $ gh student accept <assignment>

Clone that repository onto the lab machine and work in it. You practise these exact steps at the dry run.

The codebase is a **small, complete, working program in a language you have not seen before** — but one built out of the same parts as the project it follows. The Generator exam, for example, uses *Sweep*, a tiny ``sweep``/``yield`` interpreter written with ANTLR 4 and C++. It is not your own submission and not your teammates'.

This is deliberate. You cannot fall back on code you happen to remember writing, and a team whose work was unevenly divided does not get to hide that. Everything you need in order to work out what the program *should* do is in the repository:

* ``README.md`` specifies the language: its syntax, its operators, their precedence and associativity, and how to build and run it. This is the definition of correct behaviour, and it is what you check the implementation against.
* ``EXAM.md`` contains the exam tasks and their point values.
* ``tests/`` holds the test configuration and an empty directory for the tests you write. **No reference tests are shipped** — writing the tests that expose the behaviour you are looking for is part of the exam.

Read ``README.md`` first. The tasks are all stated relative to it.

What you will be asked to do
----------------------------

The tasks fall into four kinds, and one exam contains all of them:

**1. Fix a bug.** The implementation does not match the behaviour ``README.md`` specifies somewhere. You are not told where. Find it — writing tests is how — and fix it.

**2. Write a test.** You are asked for a test that distinguishes one specific behaviour from a plausible wrong one: it must pass when the implementation is correct and fail when it is not. Naming a behaviour is not enough; the test has to separate the two cases.

**3. Add a feature.** A language feature described in ``README.md`` is missing from the implementation. Implement it so that it behaves as specified, including where it interacts with features that are already there.

**4. Explain your work in writing.** A few sentences, in your own words, typed into the repository: what was broken, why your fix works, and which test exposes it. This carries marks of its own. A correct patch with no account of why it is correct does not earn them.

The coding tasks are independent. Each can be done and verified without any of the others being finished, so a task you cannot get working does not cost you the ones you can. You do not have to do them in order.

Exams are varied between students. Your neighbour's bug is not necessarily your bug, so an answer that travels across the room is worth nothing to either of you.

How it is graded
----------------

Grading weighs **understanding over syntax**. Code that clearly demonstrates the right idea but does not compile is worth more than nothing, and a fix that happens to pass while showing no grasp of the problem is worth less than full marks. Working, tested code is still the target — this is a statement about partial credit, not permission to hand in something that does not build.

**Your process is part of the grade, not only the final diff.** The commits you make, the tests you run, and the order you do things in are all visible after the fact, and partial credit is awarded for a debugging process that went somewhere even when the result is incomplete.

The practical consequence is that working the way you normally work — commit when something builds, run the tests, iterate — is worth marks. Arriving at a finished answer with nothing behind it is worth fewer.

What you may use
----------------

**AI assistants of any kind are prohibited during a lab exam.** That covers chat interfaces, editor completions backed by a hosted model, and command-line tools that call one. Using one is an academic integrity violation and is treated as such.

Reference documentation is provided **locally on the lab machines** — the C++ standard library, ANTLR, and the LLVM and MLIR headers, depending on the project. Work from it. The exam does not test whether you have memorised an API, and the local copies are there so that looking something up costs you nothing.

The machines are not network-restricted during the exam. That is a statement about how the lab works, not permission: outbound connections from your session are recorded, and reaching an AI service is as much a violation for being technically possible.

**Personal devices are put away** for the duration, under the proctors' direction. A phone in your pocket is the one channel nothing on the lab machine can see, so it is handled in the room.

Monitoring
----------

Exams are invigilated in person, and your session is recorded while you write.

At the start of the exam you run the session monitor in a terminal and leave it running until you are finished:

.. code-block:: console

   $ exammon <exam>

It is already on your ``PATH`` if you have sourced ``415env.sh``. Once a second it records the programs running under your account and the outbound network connections they open, and appends that to a log the teaching team reads. It does not read your files, your keystrokes, or your editor buffer.

Starting it is part of writing the exam. If it is not running, your session is unmonitored, and an unmonitored session is not one that can be graded with any confidence about how the work was produced.

Submitting your work
--------------------

**You are graded on what has reached GitHub by the end of the exam.** Not your working tree, not your local commits.

Push early and push often. A commit sitting unpushed on a lab machine when time is called is not a submission, and "it was finished locally" is not something anyone can verify afterwards. Since your process counts, a series of pushes across the hour is worth more to you than one at the end — and it is the cheapest insurance against the machine failing at minute fifty.

Ordinary ``git push`` to your repository's default branch is a submission. So is:

.. code-block:: console

   $ gh student submit

which snapshots your working tree into a single commit and pushes it. The two are graded the same way, so use whichever you are comfortable with.

Before the exam: the dry run
----------------------------

A dry run is held ahead of the first exam so you can confirm your setup works on a lab machine. Treat it as mandatory even if it is not.

Use it to check that:

* You can sign in at a lab machine and reach your GitHub account from it.
* ``gh student accept`` and ``gh student submit`` work for you.
* Your editor of choice starts and works there.
* You can clone, configure, build, and run a project from scratch on that machine.
* You can run ``dragon-runner`` against a test file.
* ``exammon`` starts and stays running on your session.

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
