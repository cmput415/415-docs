#!/usr/bin/env python3
"""Render a jinja-subset template against a YAML manifest.

Template syntax (a strict subset of Jinja semantics [jinja]):
  {{ dotted.path }}                     - value substitution
  {% for name in dotted.path %}...{% endfor %}
  {% if dotted.path %}...{% else %}...{% endif %}   (truthiness test)

Manifest loading prefers PyYAML [pyyaml] when importable and otherwise falls
back to a bundled block-style subset parser, so rendering never depends on a
package that bootstrap has not installed yet. The subset accepts: block
mappings and sequences (2-space indents), `- key: value` sequence items,
scalars (null/~, true/false, integers, quoted or plain strings), and
full-line comments. Flow style ({...}, [...]), anchors, and multiline
scalars are out of scope -- keep the manifest simple.

Usage: render.py MANIFEST.yaml TEMPLATE.tmpl > OUTPUT
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Union

Yaml = Union[None, bool, int, str, list["Yaml"], dict[str, "Yaml"]]
Scope = dict[str, Yaml]

# --------------------------------------------------------------- YAML loading


def _scalar(raw: str) -> Yaml:
    text = raw.strip()
    if text in ("null", "~", ""):
        return None
    if text in ("true", "false"):
        return text == "true"
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    return text


@dataclass(frozen=True)
class _Line:
    indent: int
    text: str


def _lines(source: str) -> list[_Line]:
    out: list[_Line] = []
    for raw in source.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out.append(_Line(len(raw) - len(raw.lstrip(" ")), stripped))
    return out


def _parse_block(lines: list[_Line], pos: int, indent: int) -> tuple[Yaml, int]:
    if pos >= len(lines) or lines[pos].indent < indent:
        return None, pos
    if lines[pos].text.startswith("- "):
        return _parse_seq(lines, pos, lines[pos].indent)
    return _parse_map(lines, pos, lines[pos].indent)


def _parse_map(lines: list[_Line], pos: int, indent: int) -> tuple[dict[str, Yaml], int]:
    result: dict[str, Yaml] = {}
    while pos < len(lines) and lines[pos].indent == indent and not lines[pos].text.startswith("- "):
        key, sep, rest = lines[pos].text.partition(":")
        if not sep:
            raise ValueError(f"expected 'key: value', got {lines[pos].text!r}")
        pos += 1
        if rest.strip():
            result[key.strip()] = _scalar(rest)
        else:
            result[key.strip()], pos = _parse_block(lines, pos, indent + 1)
    return result, pos


def _parse_seq(lines: list[_Line], pos: int, indent: int) -> tuple[list[Yaml], int]:
    result: list[Yaml] = []
    while pos < len(lines) and lines[pos].indent == indent and lines[pos].text.startswith("- "):
        item = lines[pos].text[2:]
        if ":" in item:
            # `- key: value` opens an inline mapping whose remaining keys sit
            # at the indent of the character after "- "
            rewritten = lines[:]
            rewritten[pos] = _Line(indent + 2, item)
            value, pos = _parse_map(rewritten, pos, indent + 2)
            result.append(value)
        else:
            result.append(_scalar(item))
            pos += 1
    return result, pos


def load_manifest(path: Path) -> Scope:
    source = path.read_text()
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(source)
    except ImportError:
        data, end = _parse_block(_lines(source), 0, 0)
        if end != len(_lines(source)):
            raise ValueError("trailing unparsed manifest content; simplify or install python3-yaml")
    if not isinstance(data, dict):
        raise ValueError("manifest must be a mapping at the top level")
    return data


# ----------------------------------------------------------------- templating

_TOKEN = re.compile(r"({{.*?}}|{%.*?%})", re.DOTALL)
_FOR = re.compile(r"^for\s+(\w+)\s+in\s+([\w.]+)$")
_IF = re.compile(r"^if\s+([\w.]+)$")


@dataclass(frozen=True)
class Text:
    value: str


@dataclass(frozen=True)
class Expr:
    path: str


@dataclass(frozen=True)
class For:
    var: str
    path: str
    body: tuple["Node", ...]


@dataclass(frozen=True)
class If:
    path: str
    body: tuple["Node", ...]
    orelse: tuple["Node", ...]


Node = Union[Text, Expr, For, If]


class TemplateError(ValueError):
    pass


def _lookup(path: str, scope: Scope) -> Yaml:
    node: Yaml = scope  # type: ignore[assignment]
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            raise TemplateError(f"unresolved path {path!r} (missing {part!r})")
        node = node[part]
    return node


def _parse(tokens: list[str], pos: int, until: frozenset[str]) -> tuple[tuple[Node, ...], int, str]:
    nodes: list[Node] = []
    while pos < len(tokens):
        tok = tokens[pos]
        if tok.startswith("{{"):
            nodes.append(Expr(tok[2:-2].strip()))
            pos += 1
        elif tok.startswith("{%"):
            stmt = tok[2:-2].strip()
            if stmt in until:
                return tuple(nodes), pos + 1, stmt
            if m := _FOR.match(stmt):
                body, pos, _ = _parse(tokens, pos + 1, frozenset({"endfor"}))
                nodes.append(For(m.group(1), m.group(2), body))
            elif m := _IF.match(stmt):
                body, pos, closer = _parse(tokens, pos + 1, frozenset({"else", "endif"}))
                orelse: tuple[Node, ...] = ()
                if closer == "else":
                    orelse, pos, _ = _parse(tokens, pos, frozenset({"endif"}))
                nodes.append(If(m.group(1), body, orelse))
            else:
                raise TemplateError(f"unsupported statement {stmt!r}")
        else:
            nodes.append(Text(tok))
            pos += 1
    if until:
        raise TemplateError(f"unterminated block, expected one of {sorted(until)}")
    return tuple(nodes), pos, ""


def _render(nodes: tuple[Node, ...], scope: Scope, out: list[str]) -> None:
    for node in nodes:
        if isinstance(node, Text):
            out.append(node.value)
        elif isinstance(node, Expr):
            value = _lookup(node.path, scope)
            if value is None or isinstance(value, (list, dict)):
                raise TemplateError(f"{node.path!r} is not a printable scalar")
            out.append(str(value))
        elif isinstance(node, For):
            seq = _lookup(node.path, scope)
            if not isinstance(seq, list):
                raise TemplateError(f"{node.path!r} is not a list")
            for item in seq:
                _render(node.body, {**scope, node.var: item}, out)
        else:
            branch = node.body if _lookup(node.path, scope) else node.orelse
            _render(branch, scope, out)


def render(template: str, scope: Scope) -> str:
    nodes, _, _ = _parse(_TOKEN.split(template), 0, frozenset())
    out: list[str] = []
    _render(nodes, scope, out)
    return "".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    scope = load_manifest(Path(argv[1]))
    sys.stdout.write(render(Path(argv[2]).read_text(), scope))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
