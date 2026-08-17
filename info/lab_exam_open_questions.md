# Lab exams — open questions

Points the student-facing lab exam page cannot answer as written. Each one is a decision, not a wording problem. Ordered by how much it blocks publishing the page.

## 1. The internet policy has no mechanism behind it

The page tells students the exam is closed-internet. Nothing enforces that.

IST has ruled out network-level control. On Jun 15 Alex Schwarzer (IST Learning Spaces) relayed that "IST Security has indicated that they are extremely reluctant to implement time based firewall rules," alongside the Director-mandated line that "The University has not implemented and is currently not planning to implement any central solution(s) to block or detect Chat GTP or other generative AI systems." On Jun 16 Nelson concluded: "It seems that they have created a policy of not providing temporary firewalls for exam purposes. This is something that we may have to discuss with the department, dean, provost, etc, but not something that we will solve for Fall 2026." The only alternative IST offered was paid AWS virtual sessions.

Jul 13 settled the direction — provide documentation locally, block only obvious cheating — but the specifics were never fixed, and on Jul 10 Ron was still describing the problem as open.

- Is the policy a rule students are told and trusted with, backed by invigilation and the auto-fail deterrent, and nothing more?
- If there is an allowed-sites list, what is on it? The page currently allows no sites at all, which is the strictest reading and the easiest to invigilate.
- Does anything technical exist at exam time, or does the page describe a rule enforced entirely socially?

The page is publishable under the strict reading. It is not publishable under a reading nobody has written down.

## 2. The monitoring script — two incompatible designs, neither built

The page says activity is monitored and defers the details to the dry run, because the two records of it describe different things.

Ayrton, Jun 16, describes staff-side monitoring: "set up a script on the cmput415 account that ssh-es into each of the machines in the lab and monitors running applications and have it flag to us when a machine runs firefox." Students do nothing.

The Jul 13 summary describes student-side monitoring: a script students run in a terminal for the duration of the exam, which clones the exam repo and logs activity including DNS lookups.

These are different systems with different failure modes, and no email after Jun 17 says either was built.

- Which one is it?
- If students run it, what happens when someone does not start it, or kills it mid-exam?
- What exactly does it log, and what are students told about that? Logging a student's activity needs a disclosure they have actually seen.

## 3. What is the set of exams?

The page deliberately does not say how many exams there are.

The Jun 11 tentative calendar has four, each in the Friday lab slot the day after the matching Thursday deadline: Generator (Sep 18), SCalc (Sep 25), VCalc (Oct 16), Gazprea (Nov 20). That calendar predates the Jul 27 pivot replacing SCalc with an LLM/parser assignment, and the Jul 27 summary carries an open action item for Nelson: "Decide on whether to hold a lab exam for the parsing assignment and add it to the to-do list, including determining the grade split between collected assignment and lab exam."

- Does the parsing assignment get an exam?
- Are the remaining dates confirmed? The Jun 11 email calls them "my suggested schedule," and no later email confirms them.
- The page says an exam falls in the Friday lab following the project deadline. Confirm that holds for Gazprea, where the Jun 11 calendar puts the exam two weeks after the Part 1 deadline rather than one.

## 4. Grade weight

Not settled anywhere. The Aug 16 thread proposes 10% for the peer evaluation and does not touch the exams; Ron's reply notes that Chloe and Ayrton wanted a quarter to a third for peer evaluation, which moves the exam number too.

The page says the weight is announced with the course outline. `info/grading.rst` has no lab exam row, so there is currently nowhere for a student to look.

## 5. How students get and submit the exam repository

The page describes taking a copy of a repository on GitHub and pushing to it, and points at the dry run for the steps, because the steps are not written down anywhere.

Classroom 50 is being set up in the `cmput415-fa26` org, with assignments "configured similarly to GitHub Classroom" (Jul 27). Nothing states the student-facing flow.

- How does a student accept the exam assignment — a link, a roster, a sign-in?
- Repo naming: student ID, CCID, or Classroom's own convention?
- How are repositories collected at the deadline, and is push access revoked at that moment or is the last commit before the timestamp taken?
- Does the `415-exams` template-cut flow still apply, or does Classroom 50 distribute the starting point itself?

The page's promise that "you are graded on your last pushed commit" depends on the answer to the third one.

## 6. What students may bring

Never discussed in any record. The page does not mention it, which means the first student to ask gets an improvised answer.

- Notes, printed or handwritten?
- Their own laptop, for anything at all?
- Their own project repository, or any code they wrote earlier?
- Their own dotfiles or editor configuration, pulled from a personal repo — which requires network access and so collides with item 1.

## 7. Accommodations

Nothing course-specific exists. The exam is a fixed 80 minutes in a fixed room on machines with a specific environment, which makes extra time and alternate sittings harder than they are for a paper exam.

- Where does a student with extra time write — the same room past the end of the lab section, or an alternate sitting?
- An alternate sitting needs a machine with the same environment and, if the exam is not to leak, a different exam. Is there a second version of each exam?

## 8. The dry run

Jul 13 lists it as an action item. No date, no procedure, no owner.

The page leans on it heavily — it is where students confirm their setup, learn the repository steps, and are shown the monitoring. If it does not happen, three sections of the page are pointing at nothing.

## 9. Mid-exam failure procedure

The page tells students to report a machine or network failure to an invigilator immediately, which is generic advice rather than a procedure.

- Does a student who loses fifteen minutes get fifteen minutes back?
- Is there a spare machine in the room, and does the student's work survive the move? (It does if everything is pushed, which is another reason the push discipline matters.)
- The paper backup covers the room being unavailable. It does not cover one machine failing at minute forty.

## 10. Academic integrity wording

The page states that using the internet or an AI assistant is an integrity violation. That sentence needs to match whatever is in the course outline, and no drafted policy text exists.

The only recorded position is Ayrton's informal "the deterrent of an auto-fail paired with this would make most (if not all) of the students behave." If auto-fail is the actual penalty, the page should say so plainly — the deterrent only works if students have read it.

## 11. Offline reference documentation

Jul 13 has an action item to prepare local copies of the C++, ANTLR, and LLVM/MLIR documentation. No email since.

The page tells students the documentation is there and that they are expected to use it. Confirm it exists, and confirm where on the machine students find it — the page should name a path.
