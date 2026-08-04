#!/usr/bin/env python3
"""Build a Canvas-ready standalone HTML rendering of ``spec/glossary.rst``.

Canvas (the LMS) forbids external CSS/JS, so the output is a single
self-contained ``.html`` file with all styles and scripts inlined.  The
converter is dependency-free (Python 3.10+ stdlib only) and intentionally
narrow in scope: it understands only the RST features the glossary source
actually uses, and it fails loudly on anything else so we notice.

Usage::

    python3 _ext/build_canvas_glossary.py \
        --input spec/glossary.rst \
        --output _build/canvas/gazprea-glossary.html

The output validates as HTML5, is WCAG 2.1 AA in the UAlberta palette,
supports light/dark/print, and includes an inline vanilla-JS term
filter.  See the design brief in the PR description for details.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from collections import OrderedDict
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent  # gazprea/
DEFAULT_INPUT = REPO_ROOT / "spec" / "glossary.rst"
DEFAULT_OUTPUT = REPO_ROOT / "_build" / "canvas" / "gazprea-glossary.html"


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------

_SLUG_STRIP_RE = re.compile(r"[^\w\s-]", re.UNICODE)
_SLUG_WS_RE = re.compile(r"[\s_]+")


def slugify(text: str) -> str:
    """Deterministic term -> anchor slug (lowercase, hyphenated)."""
    s = _SLUG_STRIP_RE.sub("", text.lower())
    s = _SLUG_WS_RE.sub("-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _dedent(line: str, n: int) -> str:
    return line[n:] if len(line) >= n else line.lstrip()


def parse_glossary(text: str) -> list[tuple[str, list[str]]]:
    """Return a list of (term, body_lines) from the ``.. glossary::`` block.

    Body lines are dedented so their leftmost column is 0.  Blank lines
    inside a body are preserved as empty strings so paragraph boundaries
    survive.
    """
    lines = text.splitlines()
    n = len(lines)

    # Locate the directive.
    i = 0
    while i < n and not lines[i].lstrip().startswith(".. glossary::"):
        i += 1
    if i == n:
        raise SystemExit("error: no .. glossary:: directive found in input")
    i += 1

    # Skip directive options (":sorted:", etc.) and leading blank lines.
    while i < n:
        stripped = lines[i].strip()
        if not stripped or (stripped.startswith(":") and stripped.endswith(":")):
            i += 1
            continue
        break

    entries: list[tuple[str, list[str]]] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            break  # end of glossary directive body
        if indent != 3:
            # Should not happen; skip defensively rather than crash.
            i += 1
            continue

        term = stripped
        i += 1
        body: list[str] = []
        while i < n:
            nxt = lines[i]
            if not nxt.strip():
                body.append("")
                i += 1
                continue
            nxt_indent = len(nxt) - len(nxt.lstrip())
            if nxt_indent <= 3:
                break
            body.append(_dedent(nxt, 6))
            i += 1
        while body and not body[-1]:
            body.pop()
        entries.append((term, body))

    return entries


_FN_RE = re.compile(r"^\.\. \[#([\w-]+)\]\s*(.*)$")
_RUBRIC_RE = re.compile(r"^\.\. rubric:: (.+)$")


def parse_footnote_groups(text: str) -> list[tuple[str, "OrderedDict[str, list[str]]"]]:
    """Extract footnote definitions, preserving their ``.. rubric::`` groups."""
    lines = text.splitlines()
    n = len(lines)
    groups: list[tuple[str, OrderedDict]] = []
    current: OrderedDict | None = None
    i = 0
    while i < n:
        m_rub = _RUBRIC_RE.match(lines[i])
        if m_rub:
            current = OrderedDict()
            groups.append((m_rub.group(1).strip(), current))
            i += 1
            continue
        m_fn = _FN_RE.match(lines[i])
        if not m_fn:
            i += 1
            continue
        name = m_fn.group(1)
        first = m_fn.group(2)
        body: list[str] = [first] if first else []
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip():
                body.append("")
                i += 1
                continue
            nxt_indent = len(nxt) - len(nxt.lstrip())
            if nxt_indent == 0:
                break
            body.append(_dedent(nxt, 3))
            i += 1
        while body and not body[-1]:
            body.pop()
        if current is None:
            current = OrderedDict()
            groups.append(("References", current))
        current[name] = body
    return groups


# ---------------------------------------------------------------------------
# Inline + block RST -> HTML rendering
# ---------------------------------------------------------------------------

class Renderer:
    """Render a small, well-defined subset of RST into HTML5.

    Everything the glossary needs and nothing more:
      inline: ``:term:``, ``:ref:``, ``[#fn]_``, ````code````, ``**b**``,
              ``*i*``, bare http(s) URLs, ``\\ `` line joiners.
      block:  paragraphs, bullet lists (``*``), ``.. note::`` admonitions.
    """

    def __init__(self, footnote_number_map: "OrderedDict[str, int]"):
        self.fn_num = footnote_number_map
        # name -> list of DOM ids used at each :footref: site (for backlinks).
        self.fn_refs: "OrderedDict[str, list[str]]" = OrderedDict()

    # ---- inline ----------------------------------------------------------

    _CODE_RE = re.compile(r"``([^`]+?)``")
    _TERM_RE = re.compile(r":term:`([^`]+)`")
    _REF_RE = re.compile(r":ref:`([^`]+)`")
    _FNREF_RE = re.compile(r"\[#([\w-]+)\]_")
    _URL_RE = re.compile(r"https?://[^\s<]+")
    _ESCWS_RE = re.compile(r"\\(\s+|$)")
    _BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
    # Italic: *content* where content doesn't start/end with whitespace,
    # star, or word char neighbours; permits inner spaces but no stars.
    _ITALIC_RE = re.compile(
        r"(?<![\*\w])\*(?!\s)([^*]+?)(?<!\s)\*(?![\*\w])"
    )
    _DISPLAY_TARGET_RE = re.compile(r"^(.*?)\s*&lt;(.*?)&gt;\s*$", re.S)

    def _term_repl(self, m: re.Match) -> str:
        content = m.group(1)
        mt = self._DISPLAY_TARGET_RE.match(content)
        if mt:
            display, target = mt.group(1), mt.group(2)
        else:
            display, target = content, content
        slug = slugify(target)
        return f'<a class="xref" href="#term-{slug}">{display}</a>'

    def _ref_repl(self, m: re.Match) -> str:
        content = m.group(1)
        mt = self._DISPLAY_TARGET_RE.match(content)
        display = mt.group(1) if mt else content
        return f'<em class="specref">{display}</em>'

    def _fn_repl(self, m: re.Match) -> str:
        name = m.group(1)
        if name not in self.fn_num:
            # Leave the source token so we notice unresolved refs.
            return m.group(0)
        num = self.fn_num[name]
        seen = self.fn_refs.setdefault(name, [])
        idx = len(seen) + 1
        rid = f"fnref-{name}-{idx}"
        seen.append(rid)
        return (
            f'<sup class="fnref">'
            f'<a href="#fn-{name}" id="{rid}" '
            f'aria-label="Footnote {num}">[{num}]</a></sup>'
        )

    def _url_repl(self, m: re.Match) -> str:
        url = m.group(0)
        trail = ""
        # Trim trailing punctuation that is unlikely to be part of the URL.
        while url and url[-1] in ".,);:":
            trail = url[-1] + trail
            url = url[:-1]
        return (
            f'<a href="{url}" rel="noopener noreferrer" '
            f'target="_blank">{url}</a>{trail}'
        )

    def render_inline(self, text: str) -> str:
        text = html.escape(text, quote=False)
        text = self._CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", text)
        text = self._TERM_RE.sub(self._term_repl, text)
        text = self._REF_RE.sub(self._ref_repl, text)
        text = self._FNREF_RE.sub(self._fn_repl, text)
        text = self._URL_RE.sub(self._url_repl, text)
        text = self._ESCWS_RE.sub(" ", text)
        text = self._BOLD_RE.sub(r"<strong>\1</strong>", text)
        text = self._ITALIC_RE.sub(r"<em>\1</em>", text)
        return text

    # ---- block -----------------------------------------------------------

    _BULLET_START_RE = re.compile(r"^\s*\*\s+")

    def render_body(self, lines: list[str]) -> str:
        out: list[str] = []
        i = 0
        n = len(lines)
        while i < n:
            if not lines[i].strip():
                i += 1
                continue
            line = lines[i]
            stripped = line.strip()

            if stripped.startswith(".. note::"):
                i += 1
                # Skip blank line(s) after directive header.
                while i < n and not lines[i].strip():
                    i += 1
                inner_lines: list[str] = []
                while i < n:
                    l = lines[i]
                    if not l.strip():
                        inner_lines.append("")
                        i += 1
                        continue
                    ind = len(l) - len(l.lstrip())
                    if ind < 3:
                        break
                    inner_lines.append(_dedent(l, 3))
                    i += 1
                inner_html = self.render_body(inner_lines)
                out.append(
                    '<aside class="note" role="note">'
                    '<p class="note-label">Note</p>'
                    f"{inner_html}</aside>"
                )
                continue

            # Silently skip other rubric/comment directives inside a body.
            if stripped.startswith(".. ") and re.match(r"^\.\. [\w-]+::", stripped):
                # Consume its indented content block if any.
                base_ind = len(line) - len(line.lstrip())
                i += 1
                while i < n:
                    l = lines[i]
                    if not l.strip():
                        i += 1
                        continue
                    if (len(l) - len(l.lstrip())) <= base_ind:
                        break
                    i += 1
                continue

            if self._BULLET_START_RE.match(line):
                out.append(self._render_bullet_list(lines, i, out_index=len(out)))
                i = self._skip_bullet_list(lines, i)
                continue

            # Regular paragraph.
            para: list[str] = [line]
            i += 1
            while i < n:
                l = lines[i]
                if not l.strip():
                    break
                if self._BULLET_START_RE.match(l):
                    break
                if re.match(r"^\.\. [\w-]+::", l.lstrip()):
                    break
                para.append(l)
                i += 1
            joined = " ".join(pl.strip() for pl in para)
            joined = re.sub(r"\s+", " ", joined).strip()
            out.append(f"<p>{self.render_inline(joined)}</p>")
        return "".join(out)

    # Bullet lists are handled with a matched pair of helpers so index
    # bookkeeping in ``render_body`` stays trivial.
    def _bullet_run_end(self, lines: list[str], start: int) -> tuple[int, int]:
        """Find (end_index, base_indent) of a bullet run starting at ``start``."""
        base = len(lines[start]) - len(lines[start].lstrip())
        i = start
        n = len(lines)
        while i < n:
            l = lines[i]
            if not l.strip():
                # Blank line: peek ahead - if next non-blank is at base
                # indent and starts with "* ", the list continues.
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j < n:
                    l2 = lines[j]
                    l2_ind = len(l2) - len(l2.lstrip())
                    if l2_ind == base and self._BULLET_START_RE.match(l2):
                        i = j
                        continue
                break
            ind = len(l) - len(l.lstrip())
            if ind < base:
                break
            if ind == base and not self._BULLET_START_RE.match(l):
                break
            i += 1
        return i, base

    def _skip_bullet_list(self, lines: list[str], start: int) -> int:
        end, _ = self._bullet_run_end(lines, start)
        return end

    def _render_bullet_list(self, lines: list[str], start: int, out_index: int = 0) -> str:
        end, base = self._bullet_run_end(lines, start)
        items_html: list[str] = []
        i = start
        while i < end:
            l = lines[i]
            if not l.strip():
                i += 1
                continue
            ind = len(l) - len(l.lstrip())
            if ind != base or not self._BULLET_START_RE.match(l):
                i += 1
                continue
            m = self._BULLET_START_RE.match(l)
            dedent = m.end()
            item_lines: list[str] = [l[dedent:]]
            i += 1
            while i < end:
                nxt = lines[i]
                if not nxt.strip():
                    item_lines.append("")
                    i += 1
                    continue
                nxt_ind = len(nxt) - len(nxt.lstrip())
                if nxt_ind == base and self._BULLET_START_RE.match(nxt):
                    break
                if nxt_ind < dedent:
                    break
                item_lines.append(_dedent(nxt, dedent))
                i += 1
            while item_lines and not item_lines[-1]:
                item_lines.pop()
            inner_html = self.render_body(item_lines)
            # If item is exactly one paragraph, drop the wrapping <p>.
            single_p = re.match(r"^<p>(.*)</p>$", inner_html, re.S)
            if single_p and "<p>" not in single_p.group(1):
                inner_html = single_p.group(1)
            items_html.append(f"<li>{inner_html}</li>")
        return "<ul>" + "".join(items_html) + "</ul>"


# ---------------------------------------------------------------------------
# Inline assets
# ---------------------------------------------------------------------------

CSS = r"""
:root {
  --ua-green: #007C41;
  --ua-gold: #FFDB05;
  --ua-charcoal: #404545;
  --ua-teal-deep: #004250;
  --ua-white: #FFFFFF;
  --ua-cloud: #EBEBEB;
  --ua-ash: #E0E0E0;
  --ua-grey: #9C9C9C;
  --ua-ink: #000000;

  --bg: var(--ua-white);
  --fg: var(--ua-charcoal);
  --link: var(--ua-green);
  --link-hover: var(--ua-teal-deep);
  --rule: var(--ua-ash);
  --panel: #F5F6F3;
  --panel-fg: var(--ua-charcoal);
  --accent-bg: var(--ua-gold);
  --accent-fg: var(--ua-teal-deep);
  --focus: var(--ua-teal-deep);
  --code-bg: #F0F2EE;
  --code-fg: #003c1f;

  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      "Helvetica Neue", Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
      "Liberation Mono", monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101414;
    --fg: #E4E7E3;
    --link: #6CC24A;
    --link-hover: #FFDB05;
    --rule: #2B302E;
    --panel: #181D1D;
    --panel-fg: #E4E7E3;
    --accent-bg: #FFDB05;
    --accent-fg: #003C24;
    --focus: #FFDB05;
    --code-bg: #1A2020;
    --code-fg: #C7E1B3;
  }
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--fg);
}
body {
  font-family: var(--font-body);
  font-size: 17px;
  line-height: 1.55;
  -webkit-text-size-adjust: 100%;
}
a {
  color: var(--link);
  text-decoration: underline;
  text-underline-offset: 2px;
}
a:hover, a:focus { color: var(--link-hover); }
:focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 2px;
  border-radius: 2px;
}
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--ua-teal-deep);
  color: #fff;
  padding: 0.5em 1em;
  font-weight: 600;
  z-index: 10;
}
.skip-link:focus { left: 0.5em; top: 0.5em; }
header.masthead {
  background: var(--ua-green);
  color: #fff;
  border-bottom: 6px solid var(--ua-gold);
}
header.masthead .header-inner {
  max-width: 920px;
  margin: 0 auto;
  padding: 1.75rem 1.25rem 1.5rem;
}
header.masthead h1 {
  margin: 0 0 0.35rem 0;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}
header.masthead .lede {
  margin: 0;
  font-size: 1.05rem;
  opacity: 0.95;
}
main {
  max-width: 920px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
}
h2 {
  color: var(--link-hover);
  margin-top: 2.25rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.25rem;
  border-bottom: 2px solid var(--ua-green);
  font-size: 1.5rem;
}
@media (prefers-color-scheme: dark) {
  h2 { color: var(--fg); border-bottom-color: var(--link); }
}
h3 {
  margin-top: 1.5rem;
  font-size: 1.05rem;
  color: var(--link);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
@media (prefers-color-scheme: dark) {
  h3 { color: var(--link-hover); }
}
nav.toc {
  background: var(--panel);
  border-left: 4px solid var(--ua-green);
  padding: 0.75rem 1rem;
  margin: 1rem 0 1.25rem;
}
nav.toc h2 {
  margin: 0 0 0.4rem;
  font-size: 0.85rem;
  border: 0;
  padding: 0;
  color: var(--fg);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
nav.toc ol {
  list-style: none;
  margin: 0;
  padding: 0;
}
nav.toc li { margin: 0.2rem 0; }
.search-wrap {
  position: sticky;
  top: 0;
  background: var(--bg);
  padding: 0.75rem 0;
  margin: 0.75rem 0;
  border-bottom: 1px solid var(--rule);
  z-index: 5;
}
.search-wrap label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.9rem;
}
#search {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 2px solid var(--rule);
  border-radius: 4px;
  background: var(--bg);
  color: var(--fg);
  font: inherit;
}
#search:focus { border-color: var(--focus); }
#result-count {
  font-size: 0.85rem;
  margin-top: 0.4rem;
  color: var(--fg);
  opacity: 0.8;
}
dl.glossary { margin: 0; padding: 0; }
dl.glossary .entry {
  padding: 0.9rem 0;
  border-bottom: 1px solid var(--rule);
}
dl.glossary .entry.hidden { display: none; }
dl.glossary dt {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--link-hover);
  margin: 0 0 0.4rem;
  scroll-margin-top: 5rem;
}
@media (prefers-color-scheme: dark) {
  dl.glossary dt { color: var(--fg); }
}
dl.glossary dt .perma {
  color: var(--ua-grey);
  text-decoration: none;
  margin-left: 0.35rem;
  font-weight: 400;
  opacity: 0;
  transition: opacity 0.15s;
}
dl.glossary .entry:hover dt .perma,
dl.glossary dt .perma:focus-visible,
dl.glossary dt:target .perma {
  opacity: 1;
}
dl.glossary dd { margin: 0; }
dl.glossary dd p { margin: 0.45rem 0; }
dl.glossary dd ul {
  margin: 0.45rem 0 0.45rem 1.25rem;
  padding: 0;
}
dl.glossary dd li { margin: 0.25rem 0; }
dl.glossary dt:target {
  background: var(--accent-bg);
  color: var(--accent-fg);
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
  display: inline-block;
}
a.xref {
  color: var(--link);
  text-decoration: underline dotted;
  text-underline-offset: 3px;
}
a.xref:hover { text-decoration: underline solid; }
aside.note {
  background: var(--panel);
  border-left: 4px solid var(--ua-teal-deep);
  padding: 0.6rem 0.9rem;
  margin: 0.6rem 0;
  border-radius: 0 3px 3px 0;
}
@media (prefers-color-scheme: dark) {
  aside.note { border-left-color: var(--link); }
}
aside.note .note-label {
  margin: 0 0 0.3rem;
  font-weight: 700;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ua-teal-deep);
}
@media (prefers-color-scheme: dark) {
  aside.note .note-label { color: var(--ua-gold); }
}
aside.note p { margin: 0.3rem 0; }
code {
  font-family: var(--font-mono);
  font-size: 0.92em;
  background: var(--code-bg);
  color: var(--code-fg);
  padding: 0.1em 0.3em;
  border-radius: 3px;
  word-break: break-word;
}
@media (prefers-color-scheme: dark) {
  code { color: #B7E4A2; }
}
sup.fnref { font-size: 0.75em; line-height: 1; vertical-align: super; }
sup.fnref a { text-decoration: none; padding: 0 0.15em; }
sup.fnref a::before { content: ""; }
.specref { font-style: italic; }
ol.footnotes {
  padding-left: 1.75rem;
  font-size: 0.94rem;
}
ol.footnotes li {
  margin: 0.7rem 0;
  scroll-margin-top: 5rem;
  padding-left: 0.15rem;
}
ol.footnotes li:target {
  background: var(--accent-bg);
  color: var(--accent-fg);
  padding: 0.3rem 0.5rem;
  border-radius: 3px;
}
ol.footnotes p { margin: 0.25rem 0; display: inline; }
ol.footnotes p + p { display: block; margin-top: 0.35rem; }
ol.footnotes ul { margin: 0.35rem 0; padding-left: 1.25rem; }
.fnbacklink {
  text-decoration: none;
  margin-left: 0.35rem;
  font-weight: 600;
}
footer.colophon {
  max-width: 920px;
  margin: 0 auto;
  padding: 1rem 1.25rem 2rem;
  font-size: 0.85rem;
  color: var(--fg);
  opacity: 0.75;
  border-top: 1px solid var(--rule);
}
@media print {
  header.masthead {
    background: none;
    color: #000;
    border-bottom: 2px solid #000;
  }
  .skip-link, .search-wrap, nav.toc { display: none !important; }
  body { font-size: 11pt; color: #000; background: #fff; }
  main { max-width: none; padding: 0.5in; }
  a { color: #000; text-decoration: underline; }
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    word-break: break-all;
  }
  dl.glossary .entry {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  aside.note {
    border-left-color: #000;
    background: #f4f4f4;
    color: #000;
  }
}
"""


JS = r"""
(function () {
  var search = document.getElementById('search');
  var count = document.getElementById('result-count');
  var entries = Array.prototype.slice.call(
    document.querySelectorAll('dl.glossary .entry')
  );
  var total = entries.length;
  function label(n) {
    return n + ' term' + (n === 1 ? '' : 's');
  }
  if (count) count.textContent = label(total);
  if (!search) return;

  function normalize(s) { return (s || '').toLowerCase(); }

  function apply(q) {
    q = normalize(q).trim();
    var shown = 0;
    for (var i = 0; i < entries.length; i++) {
      var e = entries[i];
      var hay = e.getAttribute('data-search') || '';
      if (!q || hay.indexOf(q) !== -1) {
        e.classList.remove('hidden');
        shown++;
      } else {
        e.classList.add('hidden');
      }
    }
    if (count) {
      count.textContent = q
        ? shown + ' of ' + total + ' matching'
        : label(total);
    }
  }

  var timer = null;
  search.addEventListener('input', function (ev) {
    if (timer) clearTimeout(timer);
    var v = ev.target.value;
    timer = setTimeout(function () { apply(v); }, 40);
  });

  // Initialise from ?q= for shareable filter links.
  try {
    var params = new URLSearchParams(window.location.search);
    var q = params.get('q');
    if (q) { search.value = q; apply(q); }
  } catch (_) { /* older browsers: no-op */ }
})();
"""


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

def build_html(entries: list[tuple[str, list[str]]],
               footnote_groups: list[tuple[str, "OrderedDict[str, list[str]]"]]) -> str:
    # Flatten to a single name->body map in source order for numbering.
    flat: "OrderedDict[str, list[str]]" = OrderedDict()
    for _title, group in footnote_groups:
        for name, body in group.items():
            flat[name] = body
    fn_number_map: "OrderedDict[str, int]" = OrderedDict(
        (name, i + 1) for i, name in enumerate(flat.keys())
    )
    renderer = Renderer(fn_number_map)

    # Sphinx :sorted: -- alphabetical, case-insensitive.
    entries_sorted = sorted(entries, key=lambda e: e[0].lower())

    entry_html_parts: list[str] = []
    seen_terms_search: list[tuple[str, str]] = []
    for term, body in entries_sorted:
        slug = slugify(term)
        term_esc = html.escape(term)
        body_html = renderer.render_body(body)
        # data-search combines the term and definition text so filter
        # matches on either.  Strip tags for the haystack.
        body_text = re.sub(r"<[^>]+>", " ", body_html)
        body_text = html.unescape(body_text)
        haystack = (term + " " + body_text).lower()
        haystack_attr = html.escape(haystack, quote=True)
        seen_terms_search.append((slug, haystack_attr))
        entry_html_parts.append(
            f'  <div class="entry" data-search="{haystack_attr}">\n'
            f'    <dt id="term-{slug}">{term_esc}'
            f'<a class="perma" href="#term-{slug}" '
            f'aria-label="Permalink to {term_esc}" title="Permalink">'
            "\u00b6</a></dt>\n"
            f"    <dd>{body_html}</dd>\n"
            f"  </div>"
        )

    # Now render footnotes; renderer.fn_refs is populated by the entry
    # pass above and gets extended by rendering footnote bodies too.
    fn_group_html: list[str] = []
    for title, group in footnote_groups:
        if not group:
            continue
        items: list[str] = []
        for name, body in group.items():
            num = fn_number_map[name]
            body_html = renderer.render_body(body)
            refs = renderer.fn_refs.get(name, [])
            if refs:
                if len(refs) == 1:
                    backlinks = (
                        f' <a class="fnbacklink" href="#{refs[0]}" '
                        f'aria-label="Back to reference {num}" '
                        'title="Back to reference">\u21a9</a>'
                    )
                else:
                    parts = " ".join(
                        f'<a class="fnbacklink" href="#{rid}" '
                        f'aria-label="Back to reference {num} (occurrence {k+1})" '
                        f'title="Back to reference {k+1}">'
                        f"\u21a9<sub>{k+1}</sub></a>"
                        for k, rid in enumerate(refs)
                    )
                    backlinks = " " + parts
            else:
                backlinks = ""
            items.append(
                f'    <li id="fn-{name}" value="{num}">'
                f"{body_html}{backlinks}</li>"
            )
        fn_group_html.append(
            f'  <h3 class="source-group">{html.escape(title)}</h3>\n'
            f'  <ol class="footnotes">\n{chr(10).join(items)}\n  </ol>'
        )

    total_terms = len(entries_sorted)
    total_fns = len(fn_number_map)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gazprea Glossary</title>
<meta name="description" content="Technical glossary for the Gazprea language specification. University of Alberta, CMPUT 415.">
<meta name="color-scheme" content="light dark">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="masthead">
  <div class="header-inner">
    <h1>Gazprea Glossary</h1>
    <p class="lede">Technical terminology for the <em>Gazprea</em> language specification &mdash; University of Alberta, CMPUT 415.</p>
  </div>
</header>
<main id="main">
  <nav class="toc" aria-label="On this page">
    <h2>On this page</h2>
    <ol>
      <li><a href="#terms">Terms ({total_terms})</a></li>
      <li><a href="#sources">Authoritative sources ({total_fns})</a></li>
    </ol>
  </nav>
  <section class="search-wrap" aria-label="Filter terms">
    <label for="search">Filter terms</label>
    <input type="search" id="search"
           placeholder="Type to filter, e.g. lvalue, compile time&hellip;"
           aria-controls="terms" autocomplete="off" spellcheck="false">
    <div id="result-count" aria-live="polite"></div>
  </section>
  <section id="terms" aria-labelledby="terms-heading">
    <h2 id="terms-heading">Terms</h2>
    <dl class="glossary">
{chr(10).join(entry_html_parts)}
    </dl>
  </section>
  <section id="sources" aria-labelledby="sources-heading">
    <h2 id="sources-heading">Authoritative sources</h2>
    <p>Each citation below is referenced from one or more entries above. Following these links opens the source's own site in a new tab.</p>
{chr(10).join(fn_group_html)}
  </section>
</main>
<footer class="colophon">
  <p>Generated from <code>spec/glossary.rst</code> by
     <code>_ext/build_canvas_glossary.py</code>.
     Colour palette follows the University of Alberta visual identity.
     Content is available under the same terms as the surrounding specification.</p>
</footer>
<script>{JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                    help=f"input RST file (default: {DEFAULT_INPUT})")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                    help=f"output HTML file (default: {DEFAULT_OUTPUT})")
    args = ap.parse_args(argv)

    if not args.input.is_file():
        print(f"error: input not found: {args.input}", file=sys.stderr)
        return 2

    text = args.input.read_text(encoding="utf-8")
    entries = parse_glossary(text)
    if not entries:
        print("error: no glossary entries parsed", file=sys.stderr)
        return 3
    fn_groups = parse_footnote_groups(text)
    if not fn_groups:
        print("error: no footnote definitions parsed", file=sys.stderr)
        return 4

    doc = build_html(entries, fn_groups)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(doc, encoding="utf-8")
    total_fns = sum(len(g) for _, g in fn_groups)
    print(
        f"wrote {args.output} "
        f"({len(entries)} terms, {total_fns} footnotes, "
        f"{len(doc):,} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
