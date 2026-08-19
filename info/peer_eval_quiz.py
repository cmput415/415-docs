"""Render the peer evaluation rubric as a text2qti quiz for import into Canvas.

``rubric_data.py`` is the single source for every rendering of the rubric. This
script adds one more: the form an evaluator fills out after a session, as
text2qti Markdown. Compile it to a QTI package with::

    python3 peer_eval_quiz.py --session p1 > peer_eval_p1.txt
    text2qti peer_eval_p1.txt

and import the resulting ``.zip`` through Settings > Import Course Content >
"QTI .zip file".

One quiz is one evaluator's assessment of one team: a placement on each
objective for every evaluated member, a mark and a justification for each of
them, and the same for the team as a whole.

Canvas has no matrix question type, so each placement is its own question and
the descriptors are carried in the choices. Nothing here has a right answer, so
set the imported quiz to **Graded Survey** in its settings: that awards points
for completing it and leaves a gradebook column, without scoring the responses.
Under ``--placement mc`` the first choice is marked correct because text2qti
requires a key; ``--placement numeric`` accepts any placement in ``[1, 4]``
instead and so carries no key at all.

Every question is worth text2qti's default of one point, which a graded survey
spends as a participation mark.

Marks out of 100 accept 1 to 100: a numerical question cannot admit zero, and
the lowest anchor is 35.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rubric_data

ORDINALS = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth"}

# One quiz per evaluation session. Part 2 is evaluated twice, so a part number
# alone does not name a session. The name reaches both the quiz title and the
# first question: Canvas keys a replacing import on an identifier that text2qti
# hashes from the questions alone, so two sessions whose questions match to the
# byte import as one quiz that overwrites the other.
SESSIONS = {
    "p1": ("Gazprea Part 1 Peer Evaluation", "Part 1"),
    "p2-1": ("Gazprea Part 2 Peer Evaluation 1", "Part 2"),
    "p2-2": ("Gazprea Part 2 Peer Evaluation 2", "Part 2"),
}


class Quiz:
    """Accumulates text2qti lines, numbering questions and indenting their bodies."""

    def __init__(self):
        self.lines = []
        self.number = 1

    def question(self, title, body, answer):
        """One question: a title, a list of body paragraphs, and its answer lines.

        text2qti reads a paragraph as part of the question only while it stays
        indented past the question number, so the body is aligned under it.
        """
        indent = " " * len(f"{self.number}. ")
        self.lines.append(f"Title: {title}")
        self.lines.append(f"{self.number}. {body[0]}")
        for paragraph in body[1:]:
            self.lines.append("")
            self.lines.extend(indent + line for line in paragraph.split("\n"))
        self.lines.append("")
        self.lines.extend(answer)
        self.lines.append("")
        self.number += 1

    def text(self):
        return "\n".join(self.lines).rstrip() + "\n"


ESSAY = ["____"]


def _numeric(low, high):
    return [f"= [{low}, {high}]"]


def _accepted(values):
    """A short-answer question accepting any of ``values``.

    A numerical range cannot admit zero, so a scale that starts there is
    collected as a short answer with every valid entry accepted instead.
    """
    return [f"* {value}" for value in values]


def _choices():
    return [
        ("*a)" if index == 0 else f"{chr(ord('a') + index)})")
        for index in range(len(rubric_data.LEVELS))
    ]


def _placement(quiz, objective, subject, placement_style):
    """A placement on one objective, for one student or for the team."""
    title = f"{subject} — {objective['title']}"
    body = [f"**{title}**", objective["lead"]]

    if placement_style == "numeric":
        levels = "\n".join(
            f"{index}. *{level}* — {objective['descriptors'][level]}"
            for index, level in enumerate(rubric_data.LEVELS, start=1)
        )
        body.append(levels)
        body.append("Enter the number of the level that fits.")
        quiz.question(title, body, _numeric(1, len(rubric_data.LEVELS)))
    else:
        answer = [
            f"{marker} {level} — {objective['descriptors'][level]}"
            for marker, level in zip(_choices(), rubric_data.LEVELS)
        ]
        quiz.question(title, body, answer)


def _mark(quiz, subject, placements):
    anchors = "; ".join(f"{description}, {mark}" for description, mark in rubric_data.ANCHORS)
    title = f"{subject} — mark out of 100"
    body = [
        f"**{title}**",
        f"A judgement rather than a calculation, but consistent with the {placements} placements above. "
        f"Anchors: {anchors}.",
    ]
    quiz.question(title, body, _numeric(1, 100))


def _justification(quiz, subject):
    title = f"{subject} — justification"
    body = [
        f"**{title}**",
        "What the placements and the mark rest on: which answers, which code, which moment in the session. "
        "If the mark sits away from where the placements alone would put it, explain the gap here.",
    ]
    quiz.question(title, body, ESSAY)


def _free_text(quiz, title, prompt):
    quiz.question(title, [f"**{title}**", prompt], ESSAY)


def _objectives(scope):
    return [objective for objective in rubric_data.OBJECTIVES if objective["scope"] == scope]


def build(session, members, placement_style, contribution_points):
    individual = _objectives("Individual")
    group = _objectives("Group")
    name, part = SESSIONS[session]
    quiz = Quiz()

    quiz.lines.extend([
        f"Quiz title: {name} — Evaluator Assessment",
        f"Quiz description: Your assessment of one team's {part} peer evaluation. "
        f"Fill this out individually, once for the team you evaluated. "
        f"Place each member on all {len(individual)} individual objectives and the team on both group objectives, "
        f"then give each a mark out of 100 and a written justification.",
        "",
        "Shuffle answers: false",
        "One question at a time: false",
        "",
    ])

    _free_text(quiz, "Team evaluated", f"The name or number of the team you evaluated at {name}, as it appears on the pairing schedule.")

    for member in range(1, members + 1):
        subject = f"Member {member}"
        ordinal = ORDINALS.get(member, f"{member}th")
        _free_text(quiz, f"{subject} — name", f"The name of the {ordinal} member of the evaluated team. Leave this blank if the team has no {ordinal} member.")
        for objective in individual:
            _placement(quiz, objective, subject, placement_style)
        _mark(quiz, subject, len(individual))
        _justification(quiz, subject)

    for objective in group:
        _placement(quiz, objective, "The team", placement_style)
    _mark(quiz, "The team", len(group))
    _justification(quiz, "The team")

    if contribution_points:
        for member in range(1, members + 1):
            title = f"Contribution points — member {member}"
            body = [
                f"**{title}**",
                f"Whole points awarded to member {member}, from 0 to 10. Across the team these must total ten, "
                f"so they can never come out even — this ranks the members against one another.",
            ]
            quiz.question(title, body, _accepted(range(0, 11)))

    return quiz.text()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--session", default="p1", choices=tuple(SESSIONS), help="which evaluation session this quiz is for")
    parser.add_argument("--members", type=int, default=4, help="members on the evaluated team")
    parser.add_argument("--placement", choices=("mc", "numeric"), default="mc", help="how a rubric placement is answered")
    parser.add_argument("--contribution-points", action="store_true", help="include the ten contribution points; omit when they are collected once per evaluating team")
    args = parser.parse_args()
    sys.stdout.write(build(args.session, args.members, args.placement, args.contribution_points))


if __name__ == "__main__":
    main()
