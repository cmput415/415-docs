#!/usr/bin/env python3
"""Tangle ``gazprea-example`` blocks from the spec into lit ``.gaz`` tests.

Scans the reStructuredText sources for ``.. gazprea-example::`` and
``.. gazprea-example-wrap::`` directives, turns each into a ``.gaz`` file
carrying the global lit ``// RUN:`` line and ``//CHECK:`` expectations, and
packages them all into a ``.tar.gz`` (flat, no ``lit.cfg.py``) that drops
into the solution compiler's ``tests/`` tree and runs with ``lit``.

Dependency-free (standard library only), mirroring
``build_canvas_glossary.py``, so it runs in the docs build without importing
Sphinx.  The parsing here reimplements just enough of the directive syntax
to find the blocks; the rich rendering path lives in ``gazprea_example.py``.

Usage::

    python3 _ext/tangle_examples.py \\
        --source . \\
        --output _build/examples/gazprea-examples.tar.gz

    python3 _ext/tangle_examples.py --list      # dry run: enumerate tests
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import tarfile
from pathlib import Path

# Make the sibling helper importable when run as a script (sys.path[0] is
# already this directory, but be explicit so ``python -m`` / odd cwd work).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gazprea_examples_common import (  # noqa: E402
    dedent_block,
    render_gaz,
    slugify,
    split_program_output,
)

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent  # gazprea/
DEFAULT_SOURCE = REPO_ROOT
DEFAULT_OUTPUT = REPO_ROOT / "_build" / "examples" / "gazprea-examples.tar.gz"
# Directory prefix inside the tarball so extraction is tidy (no tarbomb):
# ``tar xzf gazprea-examples.tar.gz`` yields ``gazprea-examples/*.gaz``.
ARCHIVE_PREFIX = "gazprea-examples"

_DIRECTIVE_RE = re.compile(
    r"^(?P<indent>[ \t]*)\.\. gazprea-example(?P<wrap>-wrap)?::[ \t]*$"
)
_OPTION_RE = re.compile(r"^:(?P<key>[\w-]+):[ \t]*(?P<val>.*)$")


class Example:
    """One parsed ``gazprea-example`` block."""

    __slots__ = ("source", "index", "wrap", "name", "program", "output")

    def __init__(self, source, index, wrap, name, program, output):
        self.source = source    # rst path relative to the source root
        self.index = index      # 1-based order within that file
        self.wrap = wrap        # gazprea-example-wrap -> wrap in main()
        self.name = name        # explicit :name: option, or None
        self.program = program  # program text (str)
        self.output = output    # expected stdout lines (list[str])


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def parse_file(text: str, rel: str) -> "list[Example]":
    """Extract every ``gazprea-example`` block from one RST source."""
    lines = text.splitlines()
    i, n = 0, len(lines)
    out: "list[Example]" = []
    count = 0
    while i < n:
        m = _DIRECTIVE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        base = len(m.group("indent"))
        wrap = bool(m.group("wrap"))
        i += 1

        # Options: indented ``:key: value`` lines before the first blank.
        options: "dict[str, str]" = {}
        while i < n and lines[i].strip():
            if _indent_of(lines[i]) <= base:
                break
            mo = _OPTION_RE.match(lines[i].strip())
            if not mo:
                break
            options[mo.group("key")] = mo.group("val").strip()
            i += 1

        # Skip blank line(s) separating the header/options from the body.
        while i < n and not lines[i].strip():
            i += 1

        # Body: lines indented deeper than the directive marker.
        body: "list[str]" = []
        while i < n:
            line = lines[i]
            if not line.strip():
                body.append("")
                i += 1
                continue
            if _indent_of(line) <= base:
                break
            body.append(line)
            i += 1

        body = dedent_block(body)
        program_lines, output_lines = split_program_output(body)
        count += 1
        out.append(
            Example(
                source=rel,
                index=count,
                wrap=wrap,
                name=options.get("name") or None,
                program="\n".join(program_lines),
                output=output_lines,
            )
        )
    return out


def _safe_stem(rel: str) -> str:
    """``spec/types/matrix.rst`` -> ``spec_types_matrix`` (unique per file)."""
    stem = rel[:-4] if rel.endswith(".rst") else rel
    return re.sub(r"[^\w]+", "_", stem).strip("_")


def assign_names(examples: "list[Example]") -> "list[tuple[str, Example]]":
    """Give every example a unique ``<name>.gaz`` filename.

    An explicit ``:name:`` wins (slugified); otherwise the name is derived
    from the source path plus the block's index within the file.  Collisions
    (including duplicate ``:name:`` values) get a numeric suffix.
    """
    used: "set[str]" = set()
    named: "list[tuple[str, Example]]" = []
    for ex in examples:
        if ex.name:
            base = slugify(ex.name) or _safe_stem(ex.source)
        else:
            base = f"{_safe_stem(ex.source)}_{ex.index:02d}"
        candidate, k = base, 2
        while candidate in used:
            candidate = f"{base}_{k}"
            k += 1
        used.add(candidate)
        named.append((candidate + ".gaz", ex))
    return named


def find_rst(source_root: Path) -> "list[Path]":
    """All ``.rst`` under ``source_root``, excluding build output, sorted."""
    return sorted(
        p for p in source_root.rglob("*.rst") if "_build" not in p.parts
    )


def collect(source_root: Path) -> "list[Example]":
    examples: "list[Example]" = []
    for rst in find_rst(source_root):
        rel = rst.relative_to(source_root).as_posix()
        try:
            text = rst.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"warning: cannot read {rel}: {exc}", file=sys.stderr)
            continue
        for ex in parse_file(text, rel):
            if not ex.program.strip():
                print(
                    f"warning: empty gazprea-example in {rel} "
                    f"(#{ex.index}); skipping",
                    file=sys.stderr,
                )
                continue
            examples.append(ex)
    return examples


def write_archive(named: "list[tuple[str, Example]]", output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # Reproducible archive: deterministic order, fixed mtime/mode/owner so
    # rebuilds produce byte-identical tarballs (nice for CI diffs).
    with tarfile.open(output, "w:gz", format=tarfile.GNU_FORMAT) as tar:
        for fname, ex in named:
            data = render_gaz(ex.program, ex.output, ex.wrap).encode("utf-8")
            info = tarfile.TarInfo(f"{ARCHIVE_PREFIX}/{fname}")
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument(
        "--source", type=Path, default=DEFAULT_SOURCE,
        help=f"RST source root to scan (default: {DEFAULT_SOURCE})",
    )
    ap.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"output .tar.gz (default: {DEFAULT_OUTPUT})",
    )
    ap.add_argument(
        "--list", action="store_true",
        help="list the tests that would be generated; write nothing",
    )
    args = ap.parse_args(argv)

    source_root = args.source.resolve()
    if not source_root.is_dir():
        print(f"error: source not found: {source_root}", file=sys.stderr)
        return 2

    examples = collect(source_root)
    if not examples:
        print(
            f"error: no gazprea-example directives found under {source_root}",
            file=sys.stderr,
        )
        return 1

    named = assign_names(examples)

    if args.list:
        for fname, ex in named:
            kind = "wrap" if ex.wrap else "full"
            nchecks = sum(1 for l in ex.output if l.strip())
            print(f"{fname:44s} {kind:4s} {nchecks:2d} check(s)  <- {ex.source}")
        return 0

    write_archive(named, args.output)
    files = len({ex.source for _, ex in named})
    total_checks = sum(1 for _, ex in named for l in ex.output if l.strip())
    print(
        f"wrote {args.output} "
        f"({len(named)} tests from {files} file(s), "
        f"{total_checks} CHECK line(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
