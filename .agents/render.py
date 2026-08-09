#!/usr/bin/env python3
"""Render a Jinja2 template against a YAML manifest.

Usage: render.py MANIFEST.yaml TEMPLATE.tmpl > OUTPUT

Dependencies (`jinja2`, `PyYAML`) are declared in the repo's pyproject.toml
and provisioned by `uv sync`; run this script under `uv run` from a fresh
checkout so those are guaranteed available.
"""
from __future__ import annotations

import sys
from pathlib import Path

import jinja2
import yaml


def render(manifest_path: Path, template_path: Path) -> str:
    scope = yaml.safe_load(manifest_path.read_text())
    if not isinstance(scope, dict):
        raise ValueError("manifest must be a mapping at the top level")
    # Comment delimiter is remapped away from `{# #}` because the default
    # collides with bash array-length syntax `${#name[@]}` in shell templates.
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_path.parent)),
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
        comment_start_string="{##",
        comment_end_string="##}",
    )
    return env.get_template(template_path.name).render(scope)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    sys.stdout.write(render(Path(argv[1]), Path(argv[2])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
