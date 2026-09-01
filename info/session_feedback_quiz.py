"""Render the session feedback form as a text2qti quiz for import into Canvas.

One quiz is one evaluated student's account of how the team that evaluated them
ran the session: a mark out of 100 for the evaluating team with a justification,
whether they were personally given a fair chance to show their ability, and a
few factual questions about how the session went. Every member of an evaluated
team fills out their own.

Compile it to a QTI package with::

    python3 session_feedback_quiz.py --session p1 > session_feedback_p1.txt
    text2qti session_feedback_p1.txt

and import the resulting ``.zip`` through Settings > Import Course Content >
"QTI .zip file", then apply the Canvas settings listed in ``qti_quiz.py``.

The form is due before the evaluators submit their own assessments, so a
student rates the session without knowing the mark it earned them.

Three answers are read on their own rather than through the evaluating team's
mark: the serious-conduct question, which reaches the instructor; the
fair-chance question, where one member reporting that their work went untested
is the finding even when their teammates report otherwise; and the three
required questions, which are owed to each member individually, so an unticked
box names both the requirement missed and the student it was missed for.

Canvas accepts a blank answer, so a question is optional by saying so in its
prompt.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import qti_quiz
import rubric_data
from qti_quiz import SESSIONS

DURATIONS = [
    "The full hour, or close to it",
    "Around 45 minutes",
    "Around half an hour",
    "Less than half an hour",
]

FAIR_CHANCE = [
    "Yes — I had every chance to show what I knew.",
    "Mostly — I showed most of what I knew, but some of my work never came up.",
    "Partly — only a small part of my work was tested.",
    "No — I was not given a real chance to show my ability.",
]

ATTENDANCE = [
    "All of them were there for the whole session.",
    "Some arrived late or left early.",
    "Some did not attend at all.",
]


def _choice_question(quiz, title, prompt, labels):
    quiz.question(title, [f"**{title}**", prompt], qti_quiz.choices(labels))


def build(session):
    name, part = SESSIONS[session]
    quiz = qti_quiz.Quiz(
        f"{name} — Session Feedback as Evaluee (Required)",
        f"Your account of how the team that evaluated you ran your {part} peer evaluation. "
        f"Fill this out individually: every member of the evaluated team fills out their own. "
        f"It is due shortly after the session ends.",
    )

    quiz.free_text(
        "Team that evaluated you",
        f"The name or number of the team that evaluated you at {name}, as it appears on the pairing schedule.",
    )

    quiz.free_text(
        "Anything the instructor should know about",
        "Leave this blank if nothing happened. This question is for anything serious: evaluators who did not "
        "arrive or who left early, hostility, being prevented from navigating your own code, or anything else "
        "that stopped the session from running. It reaches the instructor directly and is separate from the "
        "mark you give below.",
    )

    _choice_question(
        quiz,
        "Length of the Q&A",
        "Roughly how long did the Q&A run, leaving out setup and changing rooms? The Q&A is allotted about an hour.",
        DURATIONS,
    )

    _choice_question(
        quiz,
        "A fair chance to show your ability",
        "Over the session as a whole, were you asked enough about your own work for what you understand to be clear?",
        FAIR_CHANCE,
    )

    quiz.free_text(
        "More on the chance you were given",
        "Optional. What did or did not get tested: the parts of your work that never came up, or a question you "
        "wish you had been asked.",
    )

    _choice_question(
        quiz,
        "Evaluator attendance",
        "Were the members of the evaluating team present for the session?",
        ATTENDANCE,
    )

    quiz.question(
        "The three required questions",
        [
            "**The three required questions**",
            "Every member of an evaluated team is asked all three of these at every session. Tick each one you "
            "were personally asked; leave unticked any you were not.",
        ],
        qti_quiz.checklist(rubric_data.REQUIRED_QUESTIONS),
    )

    quiz.question(
        "Areas the evaluators asked about",
        [
            "**Areas the evaluators asked about**",
            "Tick every area your team was asked about. The evaluators are required to reach all of them before "
            "the Q&A ends; leave unticked anything that never came up.",
        ],
        qti_quiz.checklist(rubric_data.COVERAGE_AREAS),
    )

    expectations = "\n".join(
        f"- **{title}** — {description}" for title, description in rubric_data.SESSION_EXPECTATIONS
    )
    anchors = "\n".join(
        f"- **{mark}** — {description}." for description, mark in rubric_data.SESSION_ANCHORS
    )
    quiz.question(
        "The evaluating team — mark out of 100",
        [
            "**The evaluating team — mark out of 100**",
            "How well the evaluating team ran the session, judged against these:",
            expectations,
            "Anchors for the mark:",
            anchors,
        ],
        qti_quiz.numeric(1, 100),
    )

    quiz.free_text(
        "The evaluating team — justification",
        "What the mark rests on: which questions, which moments in the session, and what you would have wanted "
        "done differently.",
    )

    return quiz.text()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--session", default="p1", choices=tuple(SESSIONS), help="which evaluation session this quiz is for")
    args = parser.parse_args()
    sys.stdout.write(build(args.session))


if __name__ == "__main__":
    main()
