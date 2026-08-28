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

from gazprea_examples_common import dedent_block, split_program_output


class GazpreaExample(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {"name": directives.unchanged}
    # Overridden to True by the ``-wrap`` variant; irrelevant to rendering.
    wrap = False

    def run(self):
        body = dedent_block(list(self.content))
        program_lines, output_lines = split_program_output(body)
        program_text = "\n".join(program_lines)

        result: "list[nodes.Node]" = []
        prog = nodes.literal_block(program_text, program_text)
        # Highlighting is globally disabled (highlight_language='none'); set
        # it explicitly so a future global change does not try (and fail) to
        # lex Gazprea, which Pygments does not know.
        prog["language"] = "none"
        prog["classes"].append("gazprea-example")
        result.append(prog)

        if output_lines:
            output_text = "\n".join(output_lines)
            container = nodes.container(classes=["gazprea-example-output"])
            label = nodes.paragraph(classes=["gazprea-example-output-label"])
            label += nodes.strong(text="Output")
            container += label
            out = nodes.literal_block(output_text, output_text)
            out["language"] = "none"
            container += out
            result.append(container)
        return result


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
