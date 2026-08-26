Peer Evaluation
===============

The peer evaluation is a synchronous, oral assessment of your Gazprea compiler. Your team demonstrates and defends your compiler to another team of students, who assess each of you individually and your team as a whole against the rubric on this page.

The evaluation assesses *understanding*; the number of tests you pass is graded separately. What is graded here is whether you can navigate your own code, explain why it is built the way it is, and reason about a compiler as a whole system.

Most of your result is your own: three quarters of it comes from how you personally answered, and the remaining quarter from how your team handled the questions put to it collectively.

Schedule
--------

Three evaluations are held: one for Part 1 and two for Part 2. All three follow the format described below.

In each evaluation, your team plays two roles:

* You are **evaluated** by one team.
* You **evaluate** a different team.

No team evaluates the team that evaluates them. The pairings are redrawn for every evaluation, so the team you are evaluated by and the team you evaluate are both different each time.

Evaluations run in person. Several rooms in the same building are booked for each session and teams rotate between them. The schedule for each evaluation is posted on Canvas ahead of the session: it names the team you are evaluated by, the team you evaluate, and the room for each of those two roles. Check it before the session starts.

Format
------

Each evaluation is allotted 80 minutes. About 10 minutes of that is buffer for changing rooms and setting up, leaving roughly 70 minutes across two phases.

Presentation (5-10 minutes)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your team gives a brief account of the compiler: the top-level architecture and who implemented what. Each member individually names the parts of the compiler they worked on.

This phase is not graded. It is how the evaluators learn who to direct which questions to, and a vague account of who did what leads to questions that do not match your work.

Q&A (~60 minutes)
^^^^^^^^^^^^^^^^^

The evaluators ask questions guided by the rubric and take notes as they go.

Evaluators do not see your source code before the session. You are expected to **navigate your codebase live on your own machine**, pointing at specific code to support your answers. Have your development environment open and ready — a build of the compiler, your tests, and an editor you can search in quickly. Evaluators may ask follow-up questions based on what you show them.

Four evaluators reading code over your shoulder can be cramped. Consider joining a muted Discord (or similar) call for the session instead, with every member sharing their screen for its whole duration and one member's laptop connected to the room's TV. That member switches the TV to whichever share belongs to whoever is answering. Any arrangement that lets the evaluators see the code you are pointing at will do.

Evaluators are instructed to follow up with clarifying questions when a first explanation comes out hesitant or garbled, so a rough first answer by itself does not cost you marks.

Multiple members may contribute to a single answer. Questions put to a specific member still count towards that member's own mark, though, and that mark suffers if you consistently need a teammate to answer for you.

What you will be asked
----------------------

Three kinds of questions appear in the Q&A.

**1. Questions to a specific member.** Chosen or improvised by the evaluators, aimed at the parts of the compiler you implemented. Examples of the sort of thing to expect:

* How does your compiler deal with type aliases that give a type the same name as a variable?
* How does your compiler distinguish l-values from r-values at each stage?
* Open the code that creates the basic blocks for control flow (``if``, ``loop``, and so on), and walk through what it emits.
* How are types represented in the MLIR backend?
* Do you have separate AST nodes for a global versus a local variable declaration?
* How do you handle implicit type promotion?
* How are array types handled? What type does an empty array have?

**2. Questions every member must answer.** The evaluators do not choose these; the same three are asked at every session, so you can prepare them in advance:

.. rubric-required-questions::

Each member confirms which of the three they were asked, on the form described under :ref:`sec:rating_your_evaluators`.

**3. Questions to the group.** Answered collaboratively by whichever members hold the relevant knowledge. These cover cross-cutting design. The evaluators choose their own; these are examples of the sort of thing to expect:

* How was Part 1 designed to accommodate Part 2?
* How does the AST design support the language's features?
* How is the distinction between functions and procedures enforced end-to-end?
* Take an error your compiler can report, and show us every place it passes through, from where it is detected to what the user sees.
* Where does the type system meet the AST representation, and what does each one assume about the other?

Coverage
--------

Before the Q&A ends, the evaluators must have asked at least one question touching each of:

.. rubric-coverage::

The team you evaluate is asked which of these its session reached, on the form described under :ref:`sec:rating_your_evaluators`.

Ownership expectations
----------------------

Each member must be able to speak in depth about a real share of the compiler.

Gazprea builds on the VCalc pipeline, so the work divides most naturally by language feature: one member takes arrays through the grammar, the type checker and code generation; another takes arithmetic on reals through the backend. **Split the work this way.** Splitting by compiler stage instead, with one member on the type checker and another on code generation, makes every feature wait on three or four people finishing in the right order, and teams that try it tend to stall.

When an evaluator asks about something you implemented, you can explain it at every stage it touches and point to the code that does it.

Your responsibilities as an evaluator
-------------------------------------

Evaluating is part of the exercise, and doing it badly denies the other team the chance to show what they know.

* **Submit a question list to the instructor before the lab.** Submission is required. The list is not graded on coverage; it exists so that you arrive prepared and so there is a record of it.
* **You are not bound to your list.** Ask what the session calls for, and improvise follow-ups based on what the team shows you.
* **Spread the questions.** If one person has fielded several answers already, move to a question aimed at a member who has not been tested yet. By the end, every evaluated member should have answered enough for their demonstrated understanding to be clear.
* **Draw the knowledge out.** Follow up on a weak or garbled first answer instead of recording it as a failure. A student may explain something poorly and still understand it well; your job is to find out which.
* **Track coverage as you go.** You are responsible for the coverage list above being satisfied before time runs out.

After the evaluation, each evaluator individually fills out a rubric, assigns a mark and writes a justification for each of the four evaluated students and for the team as a whole, and distributes ten contribution points across the evaluated team. All of this is described under the :ref:`grading matrix <sec:peer_eval_grading_matrix>`.

.. _sec:rating_your_evaluators:

Rating your evaluators
----------------------

Every member of the evaluated team individually fills out a short form on Canvas about how the session was run, due shortly after the session ends. It asks for one mark out of 100 for the evaluating team, with a written justification.

Anything serious — evaluators who did not arrive, hostility, or being stopped from showing your own code — goes in the second question on the form, which reaches the instructor directly.

.. _sec:peer_eval_grading_matrix:

Grading Matrix
--------------

Each evaluator produces five assessments per session: one for each of the four evaluated students, and one for the team as a whole. Each assessment has three parts.

**A filled-out rubric.** For a student, place them at one of the four levels on each of the four individual objectives. For the team, place the team at one of the four levels on each of the two group objectives.

**A mark out of 100.** For a student, this reflects their four individual placements; for the team, its two group placements. Assign it by judgement, keeping it near the anchors below.

**A written justification.** This covers both the placements and the mark, and says what they rest on — which answers, which code, which moment in the session. If the mark sits away from where the placements alone would put it, the justification is where that gap is explained.

Each evaluator also **distributes ten contribution points across the evaluated team**, individually, alongside their five assessments. The ten whole points are split among the four members according to how their contributions compared to one another, based on what the session showed. Points cannot be split in half, so ten points across four members can never come out even; every evaluator is required to rank the team. This is a relative signal only, and is separate from the marks out of 100.

Objectives and weights
^^^^^^^^^^^^^^^^^^^^^^

Four objectives are assessed for **every student individually** and make up the individual mark, a quarter each. Two are assessed **once per group** and make up the group mark, half each. The weight column below is each objective's resulting share of a student's peer result.

.. rubric-weights::

Each objective is described at four levels of performance. An evaluator places you at one of the four on each individual objective, and your team at one of the four on each group objective; the descriptors say what a level looks like.

.. rubric-levels::

The whole rubric is also laid out as a single chart, sized for printing and for use during a session: see :ref:`sec:peer_eval_rubric_chart`.

How the marks combine
^^^^^^^^^^^^^^^^^^^^^

A student's peer result is 75% their own individual mark and 25% their team's group mark. Every member therefore carries how the team performed on the cross-cutting questions, whoever answered them.

Anchors
^^^^^^^

The mark and the rubric placements must be consistent with each other. These are the reference points:

.. rubric-anchors::

Mixed placements land between the anchors. Excellent on two objectives and Good on the other two sits in the mid to high eighties. Needs improvement on one objective and Good on the rest sits near 70, and the justification should say which objective pulled the mark down.

The weight of the peer evaluation within the overall Gazprea grade is announced separately; see the :ref:`course grading matrix <sec:grading_matrix>`.

Individual objectives
^^^^^^^^^^^^^^^^^^^^^

.. rubric-objectives:: Individual

Group objectives
^^^^^^^^^^^^^^^^

.. rubric-objectives:: Group

Preparing
---------

The evaluation rewards work done throughout the project. In practice:

* **Take features end to end.** A feature you carried through the grammar, the type checker, and code generation gives you something to say at every stage of the pipeline. This is what the ownership expectations above ask of you, and it is the single largest thing you can do to prepare.
* **Work outside what you built.** The individual objectives ask you to trace features through code you did not write. Fixing a bug in a teammate's feature is the cheapest way to get there.
* **Know the reasoning behind the design.** Every objective above distinguishes describing the design from justifying it. Keep track of the decisions your team made and the alternatives you rejected.
* **Write tests you can talk about.** One objective is entirely about your tests. Be able to name a test, say what behaviour it targets, and reason about what a different failure would have told you.
* **Be able to find your code.** Live navigation is graded. Know your way around the repository without searching blindly.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.
