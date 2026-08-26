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

The chart page also gets its own stylesheet, attached here so that the rest of
the site keeps the theme's usual layout.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
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


def _objective(objective_id):
    for objective in rubric_data.OBJECTIVES:
        if objective["id"] == objective_id:
            return objective
    raise KeyError(objective_id)


class _RubricDirective(Directive):
    """Parses the lines from :meth:`lines` in the context of the calling page."""

    has_content = False

    def lines(self):
        raise NotImplementedError

    def run(self):
        parent = nodes.Element()
        self.state.nested_parse(StringList(self.lines(), source=""), self.content_offset, parent)
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
    def lines(self):
        return _bullets(rubric_data.REQUIRED_QUESTIONS)


#: The page laid out as a reference sheet by ``_static/css/rubric_sheet.css``.
SHEET_PAGE = "rubric_chart"


def _attach_sheet_css(app, pagename, templatename, context, doctree):
    if pagename == SHEET_PAGE:
        app.add_css_file("css/rubric_sheet.css")


def setup(app):
    app.add_directive("rubric-weights", RubricWeights)
    app.add_directive("rubric-levels", RubricLevels)
    app.add_directive("rubric-anchors", RubricAnchors)
    app.add_directive("rubric-objective", RubricObjective)
    app.add_directive("rubric-objectives", RubricObjectives)
    app.add_directive("rubric-chart", RubricChart)
    app.add_directive("rubric-coverage", RubricCoverage)
    app.add_directive("rubric-required-questions", RubricRequiredQuestions)
    app.connect("html-page-context", _attach_sheet_css)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
