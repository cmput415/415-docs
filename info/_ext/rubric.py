"""Directives that render the peer evaluation rubric from ``rubric_data.py``.

Each directive emits a reStructuredText ``list-table`` and hands it back to the
parser, so the output matches tables written by hand elsewhere in the docs.

- ``rubric-weights``   objective, scope and weight for all six objectives
- ``rubric-levels``    what each of the four performance levels means
- ``rubric-anchors``   the mark a given set of rubric placements is worth
- ``rubric-objective`` one objective: its lead-in and its four descriptors
- ``rubric-objectives`` every objective of a given scope, in order
- ``rubric-chart``     all objectives against all levels, as one wide grid
- ``rubric-coverage``  the areas an evaluator must ask about, as a bullet list
- ``rubric-required-questions`` the three questions every member is asked
- ``rubric-objective-titles`` every objective by title and scope, without descriptors
- ``rubric-session-expectations`` what the evaluated team judges its evaluators against
- ``rubric-session-anchors`` the mark a given quality of session is worth
- ``rubric-follow-ups`` follow-up question templates, by purpose
- ``rubric-etiquette`` how to ask, as a bullet list
- ``rubric-clock``     where the session should be at a given time
- ``rubric-tracking``  a blank grid, one row per evaluated member
- ``rubric-coverage-tracking`` the coverage areas with room to record who answered

The pages that are reference sheets rather than pages to read through get their
own stylesheets, attached here so that the rest of the site keeps the theme's
usual layout.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList

import rubric_data


def _list_table(rows, widths):
    """Render ``rows`` as a header-row list-table, one line per cell."""
    lines = [".. list-table::", "   :header-rows: 1", "   :widths: " + " ".join(str(w) for w in widths), ""]
    for row in rows:
        for index, cell in enumerate(row):
            lines.append(("   * - " if index == 0 else "     - ") + cell)
    lines.append("")
    return lines


def _bullets(items):
    return ["* " + item for item in items] + [""]


def _numbered(items):
    return ["{}. {}".format(number, item) for number, item in enumerate(items, start=1)] + [""]


def _objective(objective_id):
    for objective in rubric_data.OBJECTIVES:
        if objective["id"] == objective_id:
            return objective
    raise KeyError(objective_id)


class _RubricDirective(Directive):
    """Parses the lines from :meth:`lines` in the context of the calling page."""

    has_content = False

    #: Classes to put on the table this directive produces. The ``rst-class``
    #: directive resolves through a document-level transform, which a parse
    #: into a detached node never reaches, so the class goes on directly.
    table_classes = ()

    def lines(self):
        raise NotImplementedError

    def run(self):
        parent = nodes.Element()
        self.state.nested_parse(StringList(self.lines(), source=""), self.content_offset, parent)
        for table in parent.findall(nodes.table):
            table["classes"].extend(self.table_classes)
        return parent.children


class RubricWeights(_RubricDirective):
    def lines(self):
        rows = [["Objective", "Scope", "Weight"]]
        rows += [[o["title"], o["scope"], o["weight"]] for o in rubric_data.OBJECTIVES]
        return _list_table(rows, [60, 20, 20])


class RubricLevels(_RubricDirective):
    def lines(self):
        rows = [["Level", "Meaning"]]
        rows += [[level, rubric_data.LEVEL_MEANINGS[level]] for level in rubric_data.LEVELS]
        return _list_table(rows, [30, 70])


class RubricAnchors(_RubricDirective):
    def lines(self):
        rows = [["Rubric placement", "Mark"]] + [list(anchor) for anchor in rubric_data.ANCHORS]
        return _list_table(rows, [70, 30])


class RubricObjective(_RubricDirective):
    required_arguments = 1

    def lines(self):
        return _objective_lines(_objective(self.arguments[0]))


class RubricObjectives(_RubricDirective):
    required_arguments = 1

    def lines(self):
        scope = self.arguments[0]
        lines = []
        for objective in rubric_data.OBJECTIVES:
            if objective["scope"].lower() == scope.lower():
                lines += _objective_lines(objective)
        return lines


def _objective_lines(objective):
    lines = ["**{}.** {}".format(objective["title"], objective["lead"]), ""]
    rows = [["Level", "Descriptor"]]
    rows += [[level, objective["descriptors"][level]] for level in rubric_data.LEVELS]
    return lines + _list_table(rows, [22, 78])


class RubricChart(_RubricDirective):
    def lines(self):
        header = ["Objective"] + rubric_data.LEVELS
        rows = [header]
        for objective in rubric_data.OBJECTIVES:
            label = "**{}** ({}, {})".format(objective["title"], objective["scope"], objective["weight"])
            rows.append([label] + [objective["descriptors"][level] for level in rubric_data.LEVELS])
        return _list_table(rows, [16, 21, 21, 21, 21])


class RubricCoverage(_RubricDirective):
    def lines(self):
        return _bullets(rubric_data.COVERAGE_AREAS)


class RubricRequiredQuestions(_RubricDirective):
    #: ``:numbered:`` numbers the questions, so that a page can refer to one by
    #: its number. The tracking sheet heads its tick boxes with them.
    option_spec = {"numbered": directives.flag}

    def lines(self):
        if "numbered" in self.options:
            return _numbered(rubric_data.REQUIRED_QUESTIONS)
        return _bullets(rubric_data.REQUIRED_QUESTIONS)


class RubricObjectiveTitles(_RubricDirective):
    """Every objective by title and scope, without its descriptors.

    What an evaluator has to have evidence for by the time the session ends,
    at the size that fits on a sheet they hold during it.
    """

    def lines(self):
        rows = [["Judge each member on", "Scope"]]
        rows += [[objective["title"], objective["scope"]] for objective in rubric_data.OBJECTIVES]
        return _list_table(rows, [80, 20])


class RubricSessionExpectations(_RubricDirective):
    def lines(self):
        rows = [["The evaluating team", "What that looks like"]]
        rows += [list(expectation) for expectation in rubric_data.SESSION_EXPECTATIONS]
        return _list_table(rows, [30, 70])


class RubricSessionAnchors(_RubricDirective):
    def lines(self):
        rows = [["Mark", "The session"]]
        rows += [[mark, description] for description, mark in rubric_data.SESSION_ANCHORS]
        return _list_table(rows, [10, 90])


class RubricFollowUps(_RubricDirective):
    def lines(self):
        rows = [["To", "Ask"]] + [list(template) for template in rubric_data.FOLLOW_UP_TEMPLATES]
        return _list_table(rows, [18, 82])


class RubricEtiquette(_RubricDirective):
    def lines(self):
        return _bullets(rubric_data.ETIQUETTE)


class RubricClock(_RubricDirective):
    """The two sessions of a lab period against where each should be by then."""

    def lines(self):
        rows = [["1st", "2nd", "Where you should be"]]
        rows += [list(mark) for mark in rubric_data.SESSION_CLOCK]
        return _list_table(rows, [9, 9, 82])


#: Written into a cell that the evaluator fills in by hand. A list-table cell
#: cannot be empty, so a blank one carries a space the page does not show.
BLANK = " "


class RubricTracking(_RubricDirective):
    """One row per evaluated member, left blank to be filled in during the session."""

    #: A tick box per required question, headed by its number on the list the
    #: page prints below the grid.
    REQUIRED = [str(number) for number in range(1, len(rubric_data.REQUIRED_QUESTIONS) + 1)]

    def lines(self):
        headings = ["Member", "Areas they claim"] + self.REQUIRED
        headings += ["Questions asked", "Points", "Notes"]
        rows = [headings] + [[BLANK] * len(headings) for _ in range(4)]
        return _list_table(rows, [12, 16, 4, 4, 4, 8, 6, 30])


class RubricCoverageTracking(_RubricDirective):
    """The coverage areas with a blank beside each.

    One line of writing per area, against the several lines a member's row
    gets, so the table is named for the stylesheet to size it on its own.
    """

    table_classes = ("coverage-tracking",)

    def lines(self):
        rows = [["Area", "Who answered"]]
        rows += [[area, BLANK] for area in rubric_data.COVERAGE_AREAS]
        return _list_table(rows, [55, 45])


#: Pages laid out as reference sheets by ``_static/css/rubric_sheet.css``.
SHEET_PAGES = ("rubric_chart", "evaluator_sheet", "tracking_sheet")

#: Sheets that carry a stylesheet of their own past the shared layout, keyed by
#: page name. The tracking sheet is written on by hand and needs room to write
#: in; the cheat sheet is read from and has to fit its four tables on one side.
SHEET_CSS = {
    "tracking_sheet": "css/tracking_sheet.css",
    "evaluator_sheet": "css/evaluator_sheet.css",
}


def _attach_sheet_css(app, pagename, templatename, context, doctree):
    if pagename in SHEET_PAGES:
        app.add_css_file("css/rubric_sheet.css")
    if pagename in SHEET_CSS:
        app.add_css_file(SHEET_CSS[pagename])


def setup(app):
    app.add_directive("rubric-weights", RubricWeights)
    app.add_directive("rubric-levels", RubricLevels)
    app.add_directive("rubric-anchors", RubricAnchors)
    app.add_directive("rubric-objective", RubricObjective)
    app.add_directive("rubric-objectives", RubricObjectives)
    app.add_directive("rubric-chart", RubricChart)
    app.add_directive("rubric-coverage", RubricCoverage)
    app.add_directive("rubric-required-questions", RubricRequiredQuestions)
    app.add_directive("rubric-objective-titles", RubricObjectiveTitles)
    app.add_directive("rubric-session-expectations", RubricSessionExpectations)
    app.add_directive("rubric-session-anchors", RubricSessionAnchors)
    app.add_directive("rubric-follow-ups", RubricFollowUps)
    app.add_directive("rubric-etiquette", RubricEtiquette)
    app.add_directive("rubric-clock", RubricClock)
    app.add_directive("rubric-tracking", RubricTracking)
    app.add_directive("rubric-coverage-tracking", RubricCoverageTracking)
    app.connect("html-page-context", _attach_sheet_css)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
