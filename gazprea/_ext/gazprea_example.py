"""Sphinx directives ``gazprea-example`` and ``gazprea-example-wrap``.

They render a Gazprea code example -- and, when present, its expected
output -- into the published specification.  Authors use them in place of a
plain ``::`` literal block when the example is a *runnable* program that
should be checked against the solution compiler.

The lit ``// RUN:`` / ``//CHECK:`` scaffolding is deliberately NOT rendered
here: it exists only in the ``.gaz`` files produced by ``tangle_examples.py``
to check the examples.  See ``gazprea_examples_common.py`` for the shared
authoring format (the ``--- output ---`` separator, etc.).

``gazprea-example`` and ``gazprea-example-wrap`` render identically; the
``-wrap`` variant differs only at tangle time, where its fragment body is
wrapped in a ``main`` procedure.  The optional ``:name:`` option names the
generated ``.gaz`` file and is otherwise ignored here.
"""
from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from gazprea_examples_common import (
    dedent_block,
    parse_error_classes,
    split_program_output,
)


class GazpreaExample(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "name": directives.unchanged,
        "input": directives.unchanged,
        "error": directives.unchanged,
    }
    # Overridden to True by the ``-wrap`` variant; irrelevant to rendering.
    wrap = False

    def run(self):
        body = dedent_block(list(self.content))
        program_lines, output_lines = split_program_output(body)
        program_text = "\n".join(program_lines)
        input_str = self.options.get("input")
        error_opt = self.options.get("error")
        errors = parse_error_classes(error_opt) if error_opt else None

        result: "list[nodes.Node]" = []
        prog = nodes.literal_block(program_text, program_text)
        # Highlighting is globally disabled (highlight_language='none'); set
        # it explicitly so a future global change does not try (and fail) to
        # lex Gazprea, which Pygments does not know.
        prog["language"] = "none"
        prog["classes"].append("gazprea-example")
        result.append(prog)

        if input_str is not None:
            result.append(self._labelled_literal(
                "Input", input_str, "gazprea-example-input"))

        if errors:
            # Ill-formed example: show the expected error taxonomy in place of
            # an output block.  The tangled test only checks that an error
            # surfaces; the compiler may emit all or a subset of these.
            container = nodes.container(classes=["gazprea-example-errors"])
            label = nodes.paragraph(classes=["gazprea-example-errors-label"])
            label += nodes.strong(text="Errors")
            container += label
            para = nodes.paragraph()
            para += nodes.Text(
                "This program is ill-formed; the compiler must reject it "
                f"({', '.join(errors)})."
            )
            container += para
            result.append(container)
        elif output_lines:
            result.append(self._labelled_literal(
                "Output", "\n".join(output_lines), "gazprea-example-output"))
        return result

    @staticmethod
    def _labelled_literal(label_text, body_text, css_class):
        """A labelled literal block (used for the Input and Output panels)."""
        container = nodes.container(classes=[css_class])
        label = nodes.paragraph(classes=[css_class + "-label"])
        label += nodes.strong(text=label_text)
        container += label
        block = nodes.literal_block(body_text, body_text)
        block["language"] = "none"
        container += block
        return container


class GazpreaExampleWrap(GazpreaExample):
    wrap = True


def setup(app):
    app.add_directive("gazprea-example", GazpreaExample)
    app.add_directive("gazprea-example-wrap", GazpreaExampleWrap)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
