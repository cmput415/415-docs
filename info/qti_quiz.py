"""text2qti building blocks shared by the two peer evaluation forms.

``peer_eval_quiz.py`` renders an evaluator's assessment of the team they
evaluated; ``session_feedback_quiz.py`` renders the evaluated team's account of
how the session was run. Both are generated from ``rubric_data.py`` and
compiled by text2qti. This module holds what they have in common: the table of
sessions and the helpers that write questions.

Neither form has a right answer, so both are imported and then set to **Graded
Survey** in the quiz settings: that awards points for completing the form and
leaves a gradebook column, without scoring the responses. A multiple-choice
question still carries a key because text2qti requires one; the survey ignores
it.
"""

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

#: Answer lines for an essay question.
ESSAY = ["____"]


class Quiz(object):
    """Accumulates text2qti lines, numbering questions and indenting their bodies."""

    def __init__(self, title, description):
        self.lines = [
            f"Quiz title: {title}",
            f"Quiz description: {description}",
            "",
            "Shuffle answers: false",
            "One question at a time: false",
            "",
        ]
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

    def free_text(self, title, prompt):
        self.question(title, [f"**{title}**", prompt], ESSAY)

    def text(self):
        return "\n".join(self.lines).rstrip() + "\n"


def numeric(low, high):
    return [f"= [{low}, {high}]"]


def accepted(values):
    """A short-answer question accepting any of ``values``.

    A numerical range cannot admit zero, so a scale that starts there is
    collected as a short answer with every valid entry accepted instead.
    """
    return [f"* {value}" for value in values]


def choices(labels):
    """A multiple-choice question over ``labels``, keyed on the first."""
    return [
        ("*a) " if index == 0 else f"{chr(ord('a') + index)}) ") + label
        for index, label in enumerate(labels)
    ]


def checklist(labels):
    """A multiple-answers question over ``labels``.

    Every entry is keyed correct: the question records what happened in a
    session, so any combination of ticks is a valid response.
    """
    return [f"[*] {label}" for label in labels]
