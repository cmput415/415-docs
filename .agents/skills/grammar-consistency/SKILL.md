---
name: grammar-consistency
description: Cross-file consistency check over Gazprea grammar fragments in the spec. Use this skill whenever a change touches syntactic surface -- EBNF rules, token definitions, precedence tables, keyword lists, punctuation shapes, or example programs that exercise disputed syntax. It compares the same grammar element as it appears in different spec files (and, when present, against the reference grammar in `gazc`) and reports the divergences a human editor would catch: a rule redefined with a different RHS, a keyword listed in one chapter but treated as an identifier in another, an operator whose precedence disagrees across the precedence table and its per-operator chapter. Do NOT use this for editorial review of a single chapter (that is [[spec-review]]) or for glossary consistency (that is `spec-glossary-audit` in the memory `gazprea-glossary-source-audit`).
---

# Grammar consistency

Gazprea's syntax is currently described informally, spread across
`gazprea/spec/*.rst` and `gazprea/spec/types/*.rst`, without a single
Sphinx `.. productionlist::` directive to point at. That is precisely why
divergence is easy: a rule described in `expressions.rst` can quietly
disagree with the same rule as it appears in `types/array.rst`, and no
build step catches it.

This skill's job is to find those disagreements. It does NOT harmonize
them -- picking the correct definition is the maintainer's call.

## 1. What counts as a "grammar element"

Any syntactic surface an author might restate in more than one chapter:

- **Keywords**: reserved words listed in `keywords.rst`. Each occurrence
  of the word elsewhere in the spec should either be the keyword's own
  chapter's usage or a `` `keyword` `` literal, never an identifier in a
  code sample.
- **Operators and punctuation**: symbols with a precedence, associativity,
  or fixity claim. Cross-reference the precedence table (in
  `expressions.rst` or `type_promotion.rst`) with the per-operator
  chapters and example code.
- **Named grammar rules**: informal RHS descriptions like "an array
  literal is `[` expression-list `]`" that appear in more than one file.
  A rule with the same name but a different RHS across files is the
  primary finding this skill produces.
- **Type-form syntax**: how a type is spelled at the source level
  (`vector[N] of T`, `matrix[N,M] of T`, `T[N]`, tuple `(T, T)`,
  identifier chains). Divergent forms across `types/*.rst` and their
  users elsewhere in the spec are a common failure mode -- see PR #116
  (vector-vs-array) for a concrete instance.
- **Reserved punctuation shapes**: string/character delimiters, comment
  syntax, statement terminators.

## 2. Method

Do NOT try to rebuild a full parser from the prose. The method is
pattern-based and cross-file, not lexical:

1. **Enumerate the change surface.** From the diff (or a full-file scan
   when no diff is given), extract each grammar element the file touches.
   Store `(element, kind, file:line, RHS-or-claim-text)` rows.
2. **Find sibling occurrences.** For each element, grep the whole spec
   for other files that name the same element (case-insensitive, with
   simple morphology: singular/plural, hyphenation). Record the same
   tuple for each hit.
3. **Compare RHS/claim text.** Two occurrences agree if a human reader
   would produce the same parse from each. They diverge when: the RHS
   uses a different set of nonterminals, the operator's precedence
   number differs, the type-form's element order or delimiters differ,
   or one occurrence names a keyword the other treats as an identifier.
4. **Consult the reference implementation when present.** If
   `../gazc/` (or wherever the reference compiler lives on this
   machine) contains a grammar file (`*.g4`, `*.lark`, hand-written
   parser), compare each divergent element against it. The compiler's
   accepted form is a strong hint but is not authoritative for the
   spec -- report it as evidence, not verdict.

## 3. Report structure

Group findings by element, then by severity. For each element list every
site (`file:line`) with the RHS-or-claim excerpt, mark which pair(s)
diverge, and give a one-sentence characterization of the divergence.
Close with the machine-readable verdict:

    GRAMMAR-CONSISTENCY: agree | diverge

`diverge` when any element has two occurrences whose claims disagree;
`agree` only when every element the change surface named checked out.

## 4. Severity rubric

- **blocking**: same element, contradictory RHS/precedence/keyword-status
  across chapters -- either would be a valid parse but not both. A
  reader following the spec would produce a program the other chapter
  rejects.
- **advisory**: same element, same substance, different phrasing (e.g.
  one chapter says "comma-separated list of expressions", the other
  says "expression sequence separated by `,`"). Not wrong, but a
  liability once someone tries to edit one without the other.
- **informational**: element appears in one file only. Log so a future
  invocation can spot when a second occurrence appears.

## 5. What this skill does NOT do

- It does not propose the correct definition. Consistency is orthogonal
  to correctness; the maintainer picks which occurrence to canonicalize
  around.
- It does not lint prose. If the RHS is spelled correctly but the
  surrounding paragraph is ungrammatical, that is [[spec-review]]'s
  problem.
- It does not add `.. productionlist::` directives even when doing so
  would trivially resolve a divergence. Migrating the spec to Sphinx
  grammar directives is a separate initiative; this skill audits the
  current state.
- It does not verify grammar rules against sample programs. Extracting
  code blocks and running them through `gazc` is [[spec-review]] 2.5
  or the (unbundled) `spec-example-check` skill.

## 6. Precedent

- PR #116 (`spec(gazprea): scope the vector-array equivalence claim`)
  is the archetypal finding this skill exists to catch: two chapters
  making incompatible claims about whether a vector is (or is not) an
  array. Rerun against it as a sanity check when adjusting the
  skill's method.
- PR #118 (`refactor/precedence-single-home`) exists because the
  precedence table was previously restated in multiple chapters --
  exactly the divergence pattern this skill is designed to prevent
  from recurring.
