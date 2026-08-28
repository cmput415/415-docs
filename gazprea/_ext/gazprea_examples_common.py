"""Shared, dependency-free helpers for the Gazprea example directives.

Both the Sphinx directives (``gazprea_example.py``) and the standalone
tangler (``tangle_examples.py``) parse the same authoring convention::

    .. gazprea-example-wrap::

        integer[*] v = 1..3;
        v -> std_output;

        --- output ---
        [1 2 3]

The body holds a complete Gazprea program (``gazprea-example``) or a
statement fragment (``gazprea-example-wrap``, wrapped in a ``main``
procedure at tangle time).  An optional ``--- output ---`` separator line
splits the program from its expected stdout; every non-blank output line
becomes a ``//CHECK:`` directive in the generated ``.gaz`` lit test.

The lit ``// RUN:`` / ``//CHECK:`` scaffolding lives only in the tangled
``.gaz`` files -- it is never shown in the published specification.

This module imports only the standard library so the tangler runs in the
docs build without Sphinx/docutils, mirroring ``build_canvas_glossary.py``.
"""
from __future__ import annotations

import re

# The global lit RUN line, expanded by lit's substitutions (%gazc, %s, %t,
# %FileCheck): compile the program, run it, and match its stdout against the
# ``//CHECK:`` lines that follow.  Identical for every generated file.
RUN_LINE = "// RUN: %gazc %s %t.bin && %t.bin | %FileCheck %s"
# When an example declares no expected output we cannot pipe to FileCheck
# (it errors when a file carries zero CHECK directives), so the generated
# test only asserts the program compiles and runs to a zero exit status.
RUN_LINE_NO_OUTPUT = "// RUN: %gazc %s %t.bin && %t.bin"

# Examples that read stdin (the ``:input:`` option) get their input piped in
# from ``printf`` so each test stays a single self-contained file (no
# companion ``.ins``).  ``__INP__`` is replaced with the shell-escaped input.
RUN_INPUT = "// RUN: %gazc %s %t.bin && printf '__INP__' | %t.bin | %FileCheck %s"
RUN_INPUT_NO_OUTPUT = "// RUN: %gazc %s %t.bin && printf '__INP__' | %t.bin"

# Error examples (the ``:error:`` option) must fail to compile *or* run.
# ``not sh -c '... && ...'`` treats a failure of either stage as the expected
# outcome -- covering both compile-time errors (``error: ...``) and runtime
# traps (``IndexError: ...``) -- without depending on lit's pipefail setting.
ERROR_RUN = "// RUN: not sh -c '%gazc %s %t.bin && %t.bin' 2>&1 | %FileCheck %s"
ERROR_RUN_INPUT = (
    "// RUN: printf '__INP__' | not sh -c '%gazc %s %t.bin && %t.bin' 2>&1 "
    "| %FileCheck %s"
)
# The class is not asserted: gazc names only runtime error classes, while
# compile-time errors are a plain ``error:``.  Per the weak-testing rule the
# test only checks that *an* error surfaces -- the compiler may emit all or
# any subset of the classes the ``:error:`` option lists, which are recorded
# in a ``// Errors:`` comment for the reader.
ERROR_CHECK = "// CHECK: {{[Ee]rror:}}"

# Separator between the program and its expected stdout.  Canonical form is
# ``--- output ---``; leading dashes plus the word "output" are required so
# the line can never be mistaken for a line of Gazprea source.
OUTPUT_SEP_RE = re.compile(r"^\s*-{2,}\s*output\s*-*\s*$", re.IGNORECASE)

# FileCheck treats ``[[`` (variable) and ``{{`` (regex) specially; escape
# both so expected-output text matches literally.  Same rule the solution
# compiler's gaz26 generator uses.
_META_RE = re.compile(r"\[\[|\{\{")

_SLUG_STRIP_RE = re.compile(r"[^\w\s-]", re.UNICODE)
_SLUG_WS_RE = re.compile(r"[\s_]+")


def slugify(text: str) -> str:
    """Deterministic name -> filename-safe slug (lowercase, hyphenated)."""
    s = _SLUG_STRIP_RE.sub("", text.lower())
    s = _SLUG_WS_RE.sub("-", s)
    return s.strip("-")


def escape_filecheck(line: str) -> str:
    """Escape FileCheck metacharacters so ``line`` matches literally."""
    return _META_RE.sub(
        lambda m: "{{\\" + m.group()[0] + "\\" + m.group()[1] + "}}", line
    )


def parse_error_classes(value: str) -> list[str]:
    """Split an ``:error:`` option value into a list of error-class names.

    Accepts comma- and/or whitespace-separated names, e.g. ``TypeError`` or
    ``TypeError, CallError``.
    """
    return [c for c in re.split(r"[,\s]+", value.strip()) if c]


def _printf_arg(s: str) -> str:
    r"""Escape ``s`` for use inside ``printf '<arg>'`` in a lit RUN line.

    C-style escapes (``\n``, ``\t``, ...) are left intact for printf to
    interpret; ``%`` is doubled so printf treats it literally; single quotes
    are shell-escaped so they cannot close the surrounding quote.  The
    ``:input:`` option is therefore authored with the same ``\n``/``\t``
    notation the streams chapter already uses to describe stdin.
    """
    return s.replace("%", "%%").replace("'", "'\\''")


def dedent_block(lines: list[str]) -> list[str]:
    """Strip the common leading indentation from a block of body lines.

    Blank lines are ignored when computing the common indent and preserved
    as empty strings so paragraph structure survives.
    """
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    if not indents:
        return ["" for _ in lines]
    cut = min(indents)
    return [l[cut:] if l.strip() else "" for l in lines]


def _trim_blanks(lines: list[str]) -> list[str]:
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def split_program_output(body_lines: list[str]) -> "tuple[list[str], list[str]]":
    """Split a dedented directive body into (program, expected_output).

    The first line matching :data:`OUTPUT_SEP_RE` is the separator; lines
    above it are the program, lines below are the expected stdout.  With no
    separator the whole body is the program and ``expected_output`` is
    empty.  Leading/trailing blank lines are trimmed from each side.
    """
    sep = None
    for i, l in enumerate(body_lines):
        if OUTPUT_SEP_RE.match(l):
            sep = i
            break
    if sep is None:
        program, output = body_lines, []
    else:
        program, output = body_lines[:sep], body_lines[sep + 1:]
    return _trim_blanks(program), _trim_blanks(output)


def wrap_in_main(program_text: str) -> str:
    """Wrap a statement fragment in a runnable ``main`` procedure."""
    indented = "\n".join(
        ("    " + l) if l.strip() else "" for l in program_text.split("\n")
    )
    return (
        "procedure main() returns integer {\n"
        f"{indented}\n"
        "    return 0;\n"
        "}"
    )


def render_gaz(
    program_text: str,
    output_lines: list[str],
    wrap: bool,
    input_str: "str | None" = None,
    errors: "list[str] | None" = None,
) -> str:
    """Assemble a complete ``.gaz`` lit test from one example.

    ``wrap`` injects the ``main`` scaffold (for ``gazprea-example-wrap``).
    ``input_str`` (the ``:input:`` option) is piped to the program's stdin.
    ``errors`` (the ``:error:`` option) marks an ill-formed example: the test
    then asserts the program is *rejected* rather than matching stdout, and
    any expected output is ignored.

    Blank expected-output lines are dropped: an empty ``//CHECK:`` is a hard
    error in FileCheck and a blank line cannot be asserted as a substring.
    """
    body = wrap_in_main(program_text) if wrap else program_text

    if errors:
        run = ERROR_RUN_INPUT if input_str is not None else ERROR_RUN
        if input_str is not None:
            run = run.replace("__INP__", _printf_arg(input_str))
        parts = [
            run,
            "",
            f"// Errors: {', '.join(errors)}",
            "",
            body,
            "",
            ERROR_CHECK,
        ]
        return "\n".join(parts).rstrip("\n") + "\n"

    checks = [
        "//CHECK:" + escape_filecheck(l) for l in output_lines if l.strip() != ""
    ]
    if input_str is not None:
        run = (RUN_INPUT if checks else RUN_INPUT_NO_OUTPUT).replace(
            "__INP__", _printf_arg(input_str)
        )
    else:
        run = RUN_LINE if checks else RUN_LINE_NO_OUTPUT
    parts = [run, "", body, ""]
    parts.extend(checks)
    return "\n".join(parts).rstrip("\n") + "\n"
