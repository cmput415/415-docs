"""Peer evaluation rubric.

Single source for every rendering of the rubric. ``_ext/rubric.py`` turns this
into the per-objective tables on the Peer Evaluation page and the reference
chart on the Rubric Chart page.

Cells are rendered into reStructuredText ``list-table`` directives, so each
string must stay on one line.
"""

LEVELS = ["Excellent", "Good", "Satisfactory", "Needs improvement"]

LEVEL_MEANINGS = {
    "Excellent": "Understanding is demonstrated fluently and extends beyond what was directly asked.",
    "Good": "Understanding is solid within familiar territory, with gaps at the edges.",
    "Satisfactory": "Surface-level understanding; the *what* is present but not the *why*.",
    "Needs improvement": "The objective is not demonstrated.",
}

OBJECTIVES = [
    {
        "id": "navigate",
        "title": "Navigate and explain their work in the codebase",
        "scope": "Individual",
        "weight": "18.75%",
        "lead": "You can navigate the compiler live, point to code you worked on, and explain what it does without relying on teammates.",
        "descriptors": {
            "Excellent": "Navigates confidently and explains clearly what the code does and how it fits into the surrounding pipeline.",
            "Good": "Navigates their area well and can explain what the code does, with minor hesitation or gaps.",
            "Satisfactory": "Locates relevant code with some hesitation but gives surface-level explanations, or relies on teammates for context on parts of their own area.",
            "Needs improvement": "Cannot navigate to or explain their contributions without significant help from teammates.",
        },
    },
    {
        "id": "defend-design",
        "title": "Criticise and defend the design of their work",
        "scope": "Individual",
        "weight": "18.75%",
        "lead": "You can articulate why your section is designed the way it is, identify tradeoffs or limitations in your choices, and engage with alternatives or critiques.",
        "descriptors": {
            "Excellent": "Gives specific, reasoned justifications for their design decisions, acknowledges tradeoffs or things they would do differently, and engages with a hypothetical alternative or critique without becoming defensive or dismissive.",
            "Good": "Explains their design choices and identifies at least one tradeoff or limitation, but struggles to engage meaningfully with alternatives or critiques beyond restating what they did.",
            "Satisfactory": "Describes their design at a surface level but cannot explain why choices were made, or deflects critique without engaging with it.",
            "Needs improvement": "Cannot articulate design choices or engage with any critique of their work.",
        },
    },
    {
        "id": "tests",
        "title": "Diagnose failures and validate features through the use of tests",
        "scope": "Individual",
        "weight": "18.75%",
        "lead": "You can write a test targeting a specific compiler behaviour, explain what it is designed to catch, and use test output to reason about whether the compiler is behaving correctly.",
        "descriptors": {
            "Excellent": "Gives a concrete example of a test they wrote, explains what compiler behaviour it targets and why, and can reason about what a different failure output would imply about correct or incorrect compiler behaviour.",
            "Good": "Explains a test they wrote and interprets test output, but struggles to reason about edge cases or unfamiliar failure modes.",
            "Satisfactory": "Describes a test at a surface level but cannot reason about what a different failure output would imply, or needs significant prompting to connect test output to compiler behaviour.",
            "Needs improvement": "Cannot explain what compiler behaviour a test is designed to verify, or cannot interpret test output to draw any conclusion.",
        },
    },
    {
        "id": "information-flow",
        "title": "Outline information flow across compiler passes and identify where language features are handled",
        "scope": "Individual",
        "weight": "18.75%",
        "lead": "You can describe the role of each pass in the pipeline, explain what information is available or produced at each stage, and locate where a specific language feature is represented, checked, or emitted.",
        "descriptors": {
            "Excellent": "Gives a clear, accurate account of the pipeline as a whole and can trace an unfamiliar feature through the relevant passes without prompting.",
            "Good": "Outlines the pipeline and traces familiar features accurately, but struggles with unfamiliar features or passes they did not write.",
            "Satisfactory": "Describes individual passes but cannot connect them into a coherent account of information flow, or can only trace features they personally implemented.",
            "Needs improvement": "Cannot describe the pipeline structure or locate where a feature would be handled.",
        },
    },
    {
        "id": "unfamiliar-feature",
        "title": "Assess the implementation complexity of an unfamiliar language feature and argue a position on its design",
        "scope": "Group",
        "weight": "12.5%",
        "lead": "Given a feature that is not in the compiler, your team can reason about where it would live, what it would interact with, and what its implementation would cost — and commit to a defensible view on whether and how it should be designed.",
        "descriptors": {
            "Excellent": "Gives a specific, reasoned account of where a hypothetical feature would live and what it would cost, and argues a defensible position on its design — including tradeoffs or ways they would do it differently.",
            "Good": "Reasons about implementation complexity at a reasonable level and offers a position, but the argument is underdeveloped or not well grounded in their implementation experience.",
            "Satisfactory": "Identifies roughly where a feature would be handled but cannot reason about interactions or costs, or offers a position without any supporting argument.",
            "Needs improvement": "Cannot reason about where a new feature would be handled, or offers no position on its design.",
        },
    },
    {
        "id": "whole-compiler-design",
        "title": "Evaluate and criticise whole-compiler design decisions",
        "scope": "Group",
        "weight": "12.5%",
        "lead": "Example topics: how Part 1 was designed to accommodate Part 2; how the AST design reflects and supports the language's features; how the compiler enforces the distinction between functions and procedures end-to-end; how the type system interacts with the AST representation; how error reporting is threaded through multiple passes; how scoping and the symbol table interact across nested constructs; how type inference and promotion are handled consistently across contexts.",
        "descriptors": {
            "Excellent": "Gives clear, reasoned answers and evaluates specific choices — including acknowledging tradeoffs or things they would do differently.",
            "Good": 'Addresses questions well but struggles to justify choices beyond "it worked."',
            "Satisfactory": "Addresses questions at a surface level but cannot connect design decisions across passes, or answers are inconsistent across members.",
            "Needs improvement": "Cannot engage with cross-cutting design questions, or answers are contradictory across members.",
        },
    },
]

# Reference points tying a set of rubric placements to a mark out of 100. An
# evaluator assigns the mark by judgement and is expected to stay near these
# points.
ANCHORS = [
    ("Every objective at Excellent", "95"),
    ("Consistently Good", "80"),
    ("Consistently Satisfactory", "65"),
    ("Consistently Needs improvement", "35"),
]

# Asked of every member of an evaluated team at every session. Evaluators do
# not choose these, so students can prepare them in advance, and each member
# confirms on the session feedback form which of them they were asked.
REQUIRED_QUESTIONS = [
    "Give an example of a test you wrote, and the part of the compiler it was intended to test.",
    "Showcase what you are most proud of in your work.",
    "What did you struggle most to implement, why, and how did you solve it?",
]

# Every area an evaluator must ask about before the Q&A ends. The evaluated
# team ticks off the ones that were reached on the session feedback form, which
# is the only account of coverage that does not come from the evaluators
# themselves.
COVERAGE_AREAS = [
    "grammar and parse tree",
    "AST design and node structure",
    "symbol tables and scoping",
    "type system: checking, inference, and promotion",
    "functions versus procedures — the semantic difference and how it is enforced",
    "MLIR code generation",
    "error detection and reporting",
]

# What the evaluated team judges its evaluators against. These carry no levels:
# the evaluated team gives the evaluating team one mark for the session as a
# whole, and these say what that mark is a judgement of.
SESSION_EXPECTATIONS = [
    ("Directs questions at the right people", "Questions match the work each member said they did."),
    ("Spreads the questions across the team", "Every member is asked enough for their understanding to show."),
    ("Draws the knowledge out", "A hesitant or incomplete first answer gets a follow-up."),
    ("Covers the required ground", "Questions reach all seven coverage areas, and the group questions are substantive."),
    ("Runs the session professionally", "Starts on time, manages the clock, lets the team navigate and show its own code, and engages without hostility."),
]

# Reference points for the mark the evaluated team gives its evaluators. A
# session is judged as a whole, so these describe sessions rather than rubric
# placements.
SESSION_ANCHORS = [
    ("Ran the session as well as it could have been run: every chance to show what your team knew", "95"),
    ("Ran it well, with questions or follow-ups that could have gone further", "80"),
    ("Got through it, leaving parts of your team or of the material untested", "65"),
    ("Did not give your team a fair chance to demonstrate its work", "35"),
]

# Question shapes for the evaluator cheat sheet. The blanks are filled from
# what the team has just said, so a template carries the shape of a follow-up
# and none of its content.
FOLLOW_UP_TEMPLATES = [
    ("Clarify", "You said ______. Can you show me where that happens?"),
    ("Go deeper", "What happens if ______ instead?"),
    ("Trace", "Take ______ and walk it from the parser through to the output."),
    ("Justify", "Why ______ rather than ______? What did that cost you?"),
    ("Rescue a stall", "Let us back up: what does ______ do at all? Open the file and read it with us."),
    ("Hypothetical", "If we added ______ to the language, where would it touch first?"),
    ("Redirect", "______, you wrote ______. How does that interact with what we just heard?"),
]

# How to ask, for the cheat sheet.
ETIQUETTE = [
    "Follow up on a weak answer before you record it, and ask the same person a second way.",
    "Let a silence run a few seconds. A student who is thinking looks like a student who is stuck.",
    "Ask for the reasoning behind an answer rather than arguing with the answer.",
    "Keep your face still. The team is reading it while they talk.",
    "Ask one question at a time.",
    "Say when an answer has landed, then move on.",
]

# Where a session should be at a given time. A lab period runs two of them
# back to back, the first from 2:00 PM and the second from 3:20 PM. Each is
# allotted 80 minutes: the presentation takes 5 to 10 of them and the Q&A about
# an hour, with the rest going on changing rooms and setting up.
SESSION_CLOCK = [
    ("2:00", "3:20", "Presentation. Write down each member's name and the areas they claim."),
    ("2:10", "3:30", "Q&A opens. Start with a member who named a specific feature."),
    ("2:40", "4:00", "Halfway. Every member should have answered by now — check the tally."),
    ("3:00", "4:20", "Ten minutes left. Fill the gaps: unticked coverage areas, unasked required questions."),
    ("3:10", "4:30", "Stop. Before you leave the room: a line on each member, and the ten contribution points split across the team."),
]
