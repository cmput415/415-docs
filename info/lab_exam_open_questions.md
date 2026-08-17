# Lab exams — open questions

Points the student-facing lab exam page cannot answer as written. Each one is a decision, not a wording problem. Ordered by how much it blocks publishing the page.

## 1. The exam is one hour in three places and eighty minutes in the one that students read

`exam-monitoring/CLAUDE.md` and `exam-integrity-options.md` both state a **1-hour** exam, and the 2.5× accommodation is sized against it (2.5 hours inside a 170-minute lab block). The Jul 13 meeting summary says 1.5 hours. `GeneratorExamSolution/EXAM.md` — the text a student opens during the exam — says **80 minutes**, and its tasks are pointed 3/2/5 against that.

The page says one hour, on the strength of the two documents that agree and that the accommodation arithmetic depends on. Whichever number is right, `EXAM.md` has to be changed to match it, and the task load has to be checked against it: three coding tasks plus a written explanation in sixty minutes is a different exam from the same work in eighty.

## 2. The closed-internet rule needs an allowlist, not just a prohibition

The policy is settled: students get no internet, enforced by `exammon` rather than by any network block. The page states it that way.

A blanket prohibition cannot be literal, because the exam requires network access. Cloning the exam repository and pushing to it are git traffic to GitHub, and the page's own submission instructions depend on them. The page therefore states one exception — git traffic to the student's own exam repository — and prohibits everything else.

That makes the rule an allowlist, and the allowlist has to be agreed and matched by whatever the dashboard flags:

- Is GitHub the only permitted destination? `gh student accept` and `gh student submit` also hit the GitHub API, not only the git endpoints.
- Where does that leave benign background traffic — NTP, DNS for names the student never typed, the machine's own package or update daemons, Ubuntu telemetry? These appear under the student's session or alongside it and are not the student's doing.
- Editor traffic is the practical problem. A modern editor opens connections at startup for telemetry, update checks, and plugin sync, and a language server may fetch as it types. The page tells students to turn these off in advance, which is the right instruction and will not be followed universally. The dashboard needs a position on an editor that phones home: flag it, ignore it, or resolve it after the fact against the student.
- What is the evidentiary standard? A recorded connection to an AI service is close to conclusive. A recorded connection to an unrecognised CDN is not, and the difference should be decided before an exam produces one rather than during the appeal.

Deciding this is also what turns item 12 from a convenience into a requirement: if the open web is closed, the local documentation is the only reference students have.

## 3. `exammon` has not been validated at exam scale

`monitor/README.md` lists two validations as outstanding: cross-machine liveness (collector on one machine, dashboard on another, events visible within the NFS attribute-cache window) and scale (one collector on each of ~25 lab machines, driven by `scaletest/`). The README is explicit that the client count is the variable that matters and that co-locating collectors hides the problem.

The page now instructs every student to run `exammon <exam>` and states that an unmonitored session cannot be graded with confidence. That instruction should not ship before the scale test has run against real lab machines.

- Who runs the scale test, and by when? The first exam is the Friday after the Generator deadline.
- What is the fallback if the dashboard cannot keep up with 25 collectors — proctoring alone, or postpone the monitor to a later exam?

## 4. What is the set of exams, and what is each one worth?

The page names no count and no weight, because neither is settled.

The Jun 11 tentative calendar has four, each in the Friday lab slot after the matching Thursday deadline: Generator (Sep 18), SCalc (Sep 25), VCalc (Oct 16), Gazprea (Nov 20). That predates the Jul 27 pivot replacing SCalc with an LLM/parser assignment, and Jul 27 leaves Nelson an open item: "Decide on whether to hold a lab exam for the parsing assignment and add it to the to-do list, including determining the grade split between collected assignment and lab exam."

- Does the parsing assignment get an exam?
- Are the dates confirmed? The Jun 11 email calls them "my suggested schedule."
- The page says an exam falls in the Friday lab following the project deadline. The Jun 11 calendar puts the Gazprea exam two weeks after the Part 1 deadline, not one.
- `info/grading.rst` has no lab exam row, so a student following the page's pointer to the course outline currently finds nothing.

## 5. What counts as the process record?

The page tells students their process is graded, which follows from `exam-integrity-options.md` §5.3: "the exam environment records the debugging process — shell history, edit/compile/test timeline — and partial credit is awarded for the process, not only the final diff."

`exammon` does not record that. It records running processes and outbound TCP connections, into a spool students cannot read, designed as a monitoring and deterrence channel. It is a reasonable proxy for a compile/test timeline and no proxy at all for shell history or edit history.

- Is git history the process record students are actually graded on? If so the page is right for the wrong reason, and the grading criteria should say so plainly.
- If shell history is meant to be captured, nothing captures it yet.
- `gh student submit` snapshots the worktree into a single commit. A student who submits only that way leaves one flat commit and no process to grade — while following the page's own instructions. Either the page should push students toward ordinary `git push`, or process grading has to tolerate a single snapshot.

## 6. Per-student variation does not exist yet

`exam-integrity-options.md` adopts it (§5.2, "seed the bug in the student's own group's project code, or hand out randomized variants"), and the page now tells students that exams are varied and that a shared answer is worth nothing.

`GeneratorExamSolution` has one `exam` branch with one injected bug. There are no variants.

- Are variants per-student, per-lab-room, or per-sitting? Two rooms writing simultaneously is the minimum useful split.
- Every variant needs the task-independence check from the `exam-writing` skill run against it separately — an injected bug that is well isolated in one variant is not automatically well isolated in another.
- Variants multiply the cutting work: each one is its own `exam` branch and its own template cut.

## 7. Deadline enforcement in Classroom 50

The page promises that what has reached GitHub by the end of the exam is what counts. Nothing enforces the end.

Classroom 50's org rulesets protect default-branch history against force-push and deletion, which stops a student rewriting earlier work, but there is no deadline mechanism in what the skill documents — no automatic revocation of push access at a time.

- Is push access revoked at the end of the exam, or is the last commit before a timestamp taken?
- If it is a timestamp, note that commit dates are not protected and backdating a push is a legal fast-forward. The trustworthy signals are server-side: commit statuses, `submit/*` tags, releases, and run timestamps. Grading should read those, not commit metadata.
- `gh teacher init` sets an org Actions budget of zero with `prevent_further_usage: true`. If any part of exam collection or grading runs in Actions, it stops org-wide once included minutes are gone — and the Gazprea project's builds are not small. Set a real budget before init, or the exam infrastructure fails silently in November.

## 8. What may students bring?

Phones are now covered — they are put away under proctor direction, which the page states. The rest was never discussed.

- Notes, printed or handwritten?
- Their own project repository, or any code they wrote earlier? Pre-staged content is named as a distinct AI-access channel in `exam-integrity-options.md`, and nothing currently addresses it.
- Dotfiles or editor configuration pulled from a personal repo, which needs network access and interacts with item 2.

## 9. Accommodated sittings

The 2.5× multiplier and the requirement to finish inside the lab block are settled, and the page states both.

- Where does an accommodated student sit — the same room, or elsewhere? The same room means they are still writing after the standard sitting has finished and left, which needs a proctor to stay.
- Two staff per room, one of whom must remain for the accommodated tail. Does that work against the other room's needs?
- Does an accommodated student need a different variant? If they sit in the same room over the same period, no. If they sit separately at a different time, yes.

## 10. Mid-exam machine failure

The page tells students to report a failure to a proctor immediately, which is advice rather than a procedure.

- Does a student who loses fifteen minutes get fifteen minutes back, and against a lab block that already has to hold a 2.5-hour accommodated sitting?
- Is there a spare machine in the room? Work survives the move if it has been pushed, which is the page's argument for pushing often — but `exammon`'s log is per-student and per-exam, so a machine change is a gap in the record that needs to be reconcilable.
- The paper backup covers the room being unusable. It does not cover one machine failing at minute forty.

## 11. Academic integrity wording

The page states that AI use is an integrity violation and is treated as such. That sentence has to match the course outline, and no policy text has been drafted.

The only recorded position is Ayrton's informal "the deterrent of an auto-fail paired with this would make most (if not all) of the students behave." If auto-fail is the penalty, the page should say so plainly — a deterrent that students have not read does not deter.

Related: `exammon` records student activity into a spool students cannot read. That needs a disclosure students have actually seen, and the page's monitoring section is currently the only place it is written down.

## 12. Local reference documentation

Jul 13 has an action item to prepare local copies of the C++, ANTLR, and LLVM/MLIR documentation. Nothing since.

The page tells students the documentation is on the machines and that they should work from it, which under item 2 may be the only thing they are permitted to consult. Confirm it exists, and give the page a path to name.

## 13. The dry run

Jul 13 lists it as an action item. No date, no procedure, no owner.

The page leans on it for four things: environment check, `gh student accept`/`submit`, `exammon`, and the repository steps. If it does not happen, those sections point at nothing.
