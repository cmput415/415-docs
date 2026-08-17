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

The codebase is a **small, complete, working program in a language you have not seen before** — but one built out of the same parts as the project it follows. `Exam Vehicles <lab_exam_vehicles.html>`_ names each exam's vehicle and what it exercises. It is not your own submission and not your teammates'.

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

How it is graded
----------------

**Code is graded by building it on a lab machine and running it against a test suite you never see.** The suite is written to catch the mistakes each question is designed to expose. Pass all of it and the question is full marks, decided and done.

Fall short and your code is read by hand for partial credit. Marks there come from what the code shows: a fix that has the right idea and misses a case earns something, and one that passes by accident without addressing the problem earns less than a clean pass would.

**Code that does not build scores badly.** Nothing in the suite can run against it, so every mark has to be recovered by reading a diff, and a diff is thinner evidence than a passing test. Push something that builds, even when it is incomplete — a partial feature that compiles is worth more than a complete one that does not.

**Test-writing questions are graded by running your test twice**, against a correct build of the language and against a broken one. Your test earns its marks by reporting the intended result both times: passing on the correct build and failing on the broken one. A test that passes both times has caught nothing. A test that fails both times is not testing what it claims. Neither earns marks, so check your expected output against the specification before you settle on it.

**Written answers are graded as written answers**, and they are where marks are recovered when the code did not get there. An accurate account of what was broken and why your fix addresses it is worth marks even when the fix itself is unfinished. Do not skip them to buy coding time — they are the cheapest marks on the exam.

What you may use
----------------

**The exam is closed-internet.** The one thing you may use the network for is git traffic to your own exam repository on GitHub — cloning it at the start and pushing to it as you work. Nothing else: no web browsing, no search engines, and no AI assistants of any kind, whether a chat interface, an editor completion backed by a hosted model, or a command-line tool that calls one. Any other network use is an academic integrity violation and is treated as such.

Nothing blocks the network at the machine or the firewall. The restriction is a rule, and it is enforced by the session monitor described below, which records every outbound connection your session opens. Reaching the internet during the exam is not prevented; it is recorded.

Because of that, **turn off anything that reaches the network on its own before the exam starts**. Editor telemetry, update checks, plugin sync, and language servers that fetch as you type all produce connections under your name, and a connection you did not intend still has to be explained. If you are not sure what your editor does at startup, find out at the dry run — that is one of the things the dry run is for.

Reference documentation is provided **locally on the lab machines** — the C++ standard library, ANTLR, and the LLVM and MLIR headers, depending on the project. Work from it. The exam does not test whether you have memorised an API, and the local copies are there so that looking something up costs you nothing and costs you no network.

**The exam is open-computer.** Everything on the lab machine is yours to use, including your own home directory and everything you have put in it. Notes, a cheat sheet, and your own project repository open in a split pane for reference are all legitimate — prepare them in advance, because the exam is not the time to go looking.

**Phones and other personal devices are put away** for the duration of the exam, under the proctors' direction.

Monitoring
----------

Exams are invigilated in person, and your session is recorded while you write.

At the start of the exam you run the session monitor in a terminal and leave it running until you are finished:

.. code-block:: console

   $ exammon <exam>

It is already on your ``PATH`` if you have sourced ``415env.sh``. It records what runs on your session and what your session connects to, and reports it to the teaching team as you write.

Activity it flags brings a proctor to your desk while you are writing. After the exam, the record of your session is reviewed against what you submitted — how the work was produced, next to what was produced. The two are expected to resemble each other.

Starting it is part of writing the exam, and it is what the closed-internet rule rests on. Leave it running for the whole session. A session with no monitor record, or one whose record stops partway through, cannot be distinguished from a session that had something to hide, and it will be treated accordingly.

If it will not start, or you think it has stopped, tell a proctor rather than carrying on without it.

Submitting your work
--------------------

**You are graded on what has reached GitHub by the end of the exam.** Not your working tree, not your local commits.

Push early and push often. A commit sitting unpushed on a lab machine when time is called is not a submission, and "it was finished locally" is not something anyone can verify afterwards. A series of pushes across the hour is also the cheapest insurance you have against the machine failing at minute fifty.

Commit and ``git push`` to your repository's default branch, the same way you would on a project.

Before the exam: the dry run
----------------------------

A dry run is held ahead of the first exam so you can confirm your setup works on a lab machine. Treat it as mandatory even if it is not.

Use it to check that:

* You can sign in at a lab machine and reach your GitHub account from it.
* ``gh student accept`` works for you, and you can push to the repository it creates.
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
* **Know the commands.** Configuring a build, rebuilding after an edit, running ``dragon-runner``, committing and pushing — you should be typing these without stopping to think. Fumbling the build costs exam time that is not coming back.
* **Write yourself a cheat sheet.** The exam is open-computer, so anything you prepare beforehand is available during it. The commands you always end up looking up, a worked example of a test file, the shape of a visitor method: put them somewhere on the lab filesystem you can open in seconds.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
