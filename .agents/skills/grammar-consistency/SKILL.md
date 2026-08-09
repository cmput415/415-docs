---
name: grammar-consistency
description: English-prose consistency check over the spec. Use whenever a change touches Sphinx RST under `gazprea/spec/` (or a sibling doc directory) and you want to catch the writing-quality issues a careful copy-editor would: spelling and typos, unjustified passive voice, subject/tense drift within a paragraph, inconsistent terminology, agreement errors, and technical-writing anti-patterns (weasel words, wandering pronouns, unmotivated jargon). This skill audits English usage only -- it does NOT critique the Gazprea language grammar or its EBNF surface. Deriving the Gazprea grammar from the informal spec examples is part of the assignment for CMPUT 415 students, so keep grammar-of-Gazprea observations out of the report. Pair with [[spec-review]] for structural/build/reference review of the same files.
---

# Grammar consistency (English prose)

The Gazprea spec is written for students who then implement a compiler
from it. Ambiguity in the English prose costs student time and produces
divergent implementations; this skill catches that ambiguity before it
ships. Scope is strictly English usage in the RST sources. The Gazprea
language's own grammar is intentionally out of scope -- the exercise for
students is to derive it from the examples and clarify with the reference
compiler where needed.

## 1. What to look for

Apply the checks below to every paragraph of prose the change touches
(chapter body, admonition body, list items, table cells). Skip fenced
code samples (``.. code-block::``) and directive arguments.

### 1.1 Spelling and typography

- Real typos and misspellings (`recieve`, `seperate`, `occured`).
- Locale drift within a single file: pick either US (`initialize`,
  `behavior`) or UK (`initialise`, `behaviour`) and hold it. The spec's
  established convention is US spelling; flag UK spellings as changes to
  align, not stylistic preferences.
- Straight vs. curly quotes: RST source uses straight quotes; a curly
  quote copied in from a word processor is a build-time hazard.
- Doubled words (`the the`, `to to`) and stray whitespace inside
  sentences.
- Product/library/tool names spelled inconsistently (`Sphinx` vs.
  `sphinx`, `GitHub` vs. `Github`, `Gazprea` vs. `gazprea` when used as a
  proper noun in prose rather than a code identifier).

### 1.2 Passive voice

Passive voice is not forbidden, but it should be justified. Flag a
passive construction when:

- The agent is important and the sentence hides it ("the value is
  promoted" -- by what?), especially in normative statements.
- The passive is being used to duck a shall/must claim ("errors are
  raised" instead of "the implementation shall raise an error").
- Two consecutive sentences are both passive and could be flipped to
  active without loss.

Leave passives alone when the agent is genuinely irrelevant, when the
patient is the topic of the paragraph, or when the active form would
require inventing a subject the spec does not otherwise name.

### 1.3 Subject and tense consistency

- Subject drift inside a paragraph: `you` -> `the programmer` -> `one` ->
  `we` across three sentences forces the reader to re-resolve reference.
  Pick one and hold it for the paragraph (the spec's default is `the
  program` / `the implementation` for normative claims and `you` for
  tutorial-style prose).
- Tense drift: normative statements should stay in the present indicative
  (`the type is`, `the operator returns`), not slip into future
  (`the type will be`) or subjunctive (`the type would be`) except when
  the surrounding logic genuinely requires it.
- Number agreement: `each of the operators return` -> `returns`;
  `a list of expressions are` -> `is`.

### 1.4 Terminology consistency

- The same concept named two ways in the same file: `element type` vs.
  `component type`, `bounds check` vs. `range check`, `identity value`
  vs. `zero value`. Pick one per file (ideally per chapter) and note the
  divergence.
- Glossary terms used without `:term:` on first mention within a section.
  Cross-check against `gazprea/spec/glossary.rst`.
- Editorial synonyms creeping in ("a.k.a.", "or, equivalently", "in
  other words") that redefine a term already introduced elsewhere.

### 1.5 Technical-writing anti-patterns

- Weasel words in normative prose: `may`, `might`, `could`, `probably`,
  `should` (when the RFC 2119 meaning is intended, use `MUST`/`SHALL`
  explicitly in a `.. note::`).
- Ambiguous pronouns: `this`, `that`, `it` without an unambiguous
  antecedent in the previous sentence.
- Unmotivated jargon: a term introduced without definition on first use.
- Overloaded phrasing: `the type of the type` type constructions where a
  rewrite would flatten the sentence.
- Long sentences (>~40 words) that could be split without losing the
  logical connective; especially in normative claims.

## 2. Method

1. **Extract the prose surface** from the diff (or full-file scan). RST
   sources contain both prose and directives; strip directive bodies
   before running text checks.
2. **Run mechanical checks first** (spelling, doubled words, quote style,
   locale). These are cheap and their output frames what a human editor
   would then look at.
3. **Read the prose sequentially** to catch subject/tense/terminology
   drift; these require paragraph-level context and are not reliably
   caught by tooling.
4. **Cross-reference terminology** against `glossary.rst` and the file's
   own first-use conventions.
5. **Compose with [[spec-review]]** for anything that is structural
   rather than prose (cross-references, heading hierarchy, code-block
   correctness). Do not duplicate its findings.

## 3. Report structure

Group findings by category (spelling, passive voice, subject/tense,
terminology, anti-patterns). Within each category list `file:line`,
a one-sentence claim, and a concrete rewrite where the fix is
mechanical. Do not list what passed. Close with the machine-readable
verdict:

    GRAMMAR-CONSISTENCY: clean | advisory | blocking

`blocking` when a defect changes the meaning of a normative statement or
would confuse a student implementing from the spec; `advisory` for
readability improvements that do not change meaning; `clean` when the
prose surface the change touched has no findings.

## 4. What this skill does NOT do

- It does not comment on the Gazprea language's own grammar, EBNF, or
  syntax rules. That is the students' exercise; the spec's informal
  examples are the intended interface.
- It does not rewrite prose beyond mechanical fixes; the author decides
  substantive rewrites.
- It does not lint the code inside `.. code-block::` blocks -- that is
  [[spec-review]] 2.5 (parse/typecheck via the reference compiler).
- It does not enforce a house style guide that is not documented in this
  file. If the repo adds a `STYLE.md`, port the checks here rather than
  inventing them ad hoc.

## 5. Composition

- Run [[spec-review]] first for structural/build issues, then this skill
  for prose quality. A file that is structurally broken (build fails, refs
  unresolved) is not worth a prose pass yet.
- If the change touches only prose, this skill runs first and
  [[spec-review]] runs as a lighter follow-up (skip the parse-block
  step).
