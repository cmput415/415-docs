---
name: spec-review
description: Systematic editorial and structural review of one or more Sphinx source files in `gazprea/spec/`. Use this skill whenever you are asked to review, audit, sanity-check, or "read through" spec content in this repository -- including PR review over spec changes, pre-merge checks on a feature branch, or a fresh pass over an existing chapter. It defines the checklist a careful maintainer applies: heading hierarchy, cross-reference (`:ref:`, `:term:`, `:doc:`) integrity, glossary term coverage, admonition usage, RST directive correctness, unresolved TODO/FIXME/XXX markers, and a `gazc`-backed sanity check on inline Gazprea code blocks. Do NOT use this skill for grammar-fragment cross-consistency (that is [[grammar-consistency]]) or for glossary entry sourcing (that is the workflow in the memory `gazprea-glossary-source-audit`).
---

# Spec review

You are reviewing Sphinx-format specification source in `gazprea/spec/`. The
goal is the review a human editor performs before a chapter merges: catch
structural problems, broken cross-references, missing glossary links, and
code examples that no longer parse -- without rewriting the author's prose.

Scope this skill to spec content only (`gazprea/spec/**/*.rst`,
`gazprea/index.rst`). Non-spec RST (`base/`, `template/`, `info/`, other
languages under `scalc/`, `vcalc/`, `generator/`) is out of scope; if the
change touches those, note it and stop.

## 1. Report structure

Report findings in one grouped list, most-severe first. For each finding
give: file:line, category, one-sentence claim, and one concrete example of
how it manifests (what the reader sees, what breaks). Do not list what
passed -- silence means "checked, fine". End with a single-line verdict:

    SPEC-REVIEW: clean | advisory | blocking

`blocking` when any finding would break the Sphinx build or a normative
claim; `advisory` for everything else; `clean` only when the checklist
below ran end-to-end with no findings.

## 2. The checklist

Apply these in order. Skip a section only when it does not apply (e.g. no
code blocks in the file), and say so in the report.

### 2.1 Build integrity

- `uv run sphinx-build -W -n -b html gazprea _build/spec-review` must
  succeed. `-W` promotes warnings to errors, `-n` catches nitpicky
  cross-reference misses. If it fails, that failure is the top finding
  and the rest of the review runs against whatever survived.
- Any RST parse error, unknown directive, or unresolved `:ref:` /
  `:term:` / `:doc:` reference is `blocking`.

### 2.2 Heading hierarchy

- Underline characters must form a consistent hierarchy within a file.
  Sphinx accepts any set of characters, but re-using a character at a
  different level in the same file collapses the TOC.
- Chapter files (top of `gazprea/spec/`) use `=` for the title, `-` for
  sections, `~` for subsections, `^` for subsubsections. Nested files
  under `types/` inherit from their parent -- do not restart at `=`.
- A single `=` title per file; skip a level (title, then `~`
  subsubsection) is `blocking` because Sphinx silently promotes.

### 2.3 Cross-references

- Every normative term the file uses -- "L-value", "R-value",
  "promotion", "constant expression", "identity value", etc. -- should
  be a `:term:` link to `glossary.rst` on its first meaningful mention
  in the file. Repeat mentions in the same section do not need to
  re-link.
- Chapter-to-chapter references use `:doc:`, not raw text. Section
  references use `:ref:` against an explicit label
  (`.. _section-label:`) placed immediately above the heading.
- A `:term:` reference whose target does not exist in `glossary.rst` is
  `blocking`. A missing `:term:` on a first mention of a defined term
  is `advisory`.

### 2.4 Admonitions and directives

- Normative statements ("must", "shall") that are hidden in prose
  should be lifted into `.. note::`, `.. warning::`, or `.. important::`
  where the surrounding paragraphs make the emphasis worthwhile. Do
  not over-lift; over-use of admonitions dilutes their signal.
- `.. code-block:: gazprea` is the correct language tag for inline
  Gazprea samples (not `gz`, not `gazp`). Fenced examples without a
  language tag lose syntax highlighting and are `advisory`.

### 2.5 Code examples parse

- Extract every ` .. code-block:: gazprea ` block in the file to a temp
  directory, one file per block, and run `gazc --parse-only` (or
  `--typecheck` when the block is a full program) on each. A block that
  fails to parse or typecheck is `blocking` unless the surrounding
  prose explicitly marks it as intentionally invalid ("this program is
  rejected because..."). Store the parser output next to the extracted
  file for the report.
- Do not attempt to lower or execute; parse/typecheck is enough for
  spec review. Execution semantics belong in the test corpus.

### 2.6 TODO / FIXME / XXX / editorial residue

- `TODO`, `FIXME`, `XXX`, `NOTE:`, or bracketed `[ ... ]` placeholders
  in shipping spec text are `blocking`. Comments-out placeholders in
  RST (`.. TODO:`) are `advisory` -- flag but do not block.
- Trailing whitespace, tab characters (RST wants spaces), and mixed
  indent within a directive body are `advisory`.

### 2.7 Consistency with sibling files

- If the file describes behavior that another file also describes
  (e.g. `types/array.rst` and `types/vector.rst` on element-type
  rules), spot-check that the two do not contradict. This is a
  targeted check, not an exhaustive cross-file diff; that is
  [[spec-lattice-consistency]] territory.
- If the file names a grammar fragment, delegate the fragment's
  consistency to [[grammar-consistency]] and note in the report that
  the delegation happened.

## 3. Invocation contract

The skill is invoked with a set of one or more files (a chapter, a
subsection, or a diff). Default to reviewing all files under
`gazprea/spec/` if no scope is given.

For a PR review, restrict the code-example parse check to blocks that
were added or modified in the diff -- rerunning `gazc` over unchanged
blocks recomputes existing state and rarely surfaces new findings.

## 4. What this skill does NOT do

- It does not rewrite prose. Findings describe the problem; the author
  fixes it. If a fix is trivial and mechanical (a broken `:term:`
  target, a wrong language tag), propose the exact edit in the finding.
- It does not check normative correctness against the reference
  implementation. That is a separate `spec-example-check` skill (not
  bundled).
- It does not enforce style guide preferences that are not in this
  checklist. If the repository grows a `STYLE.md`, add the checks
  here; do not invent them ad hoc.
