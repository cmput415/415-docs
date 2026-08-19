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

# Reference points tying a set of rubric placements to a mark out of 100. The
# mark is a judgement rather than a calculation, so these are the points an
# evaluator is expected to stay near, not a formula.
ANCHORS = [
    ("Every objective at Excellent", "95"),
    ("Consistently Good", "80"),
    ("Consistently Satisfactory", "65"),
    ("Consistently Needs improvement", "35"),
]
