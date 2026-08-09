#!/usr/bin/env bash
# Run the same checks CI runs, locally, before pushing a spec change.
#
# Mirrors:
#   .github/workflows/deploySite.yml   -- Sphinx html+latexpdf across all doc
#                                          subdirs (setup, generator, lolcode,
#                                          vcalc, gazprea, info).
#   .github/workflows/linkcheck.yml    -- lychee over **/*.{md,rst,html,tex}
#                                          with the CI arg set.
#
# Usage:
#   .agents/skills/spec-review/check-ci.sh [sphinx|links|all]
#
# Default is `all`. Exits non-zero on the first failing check.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
cd "${REPO_ROOT}"

# Match the DIRS variable in the top-level Makefile so we build the exact set
# CI builds. Update in lockstep with Makefile:DIRS if that list changes.
SPHINX_DIRS=(setup generator lolcode vcalc gazprea info)

# Match lychee-action's `args:` field in linkcheck.yml exactly.
LYCHEE_ARGS=(--verbose --no-progress --exclude-path base/index.html --exclude-all-private)
LYCHEE_GLOBS=('**/*.md' '**/*.rst' '**/*.html' '**/*.tex')

failures=0
step_fail() { printf '[check-ci] FAIL: %s\n' "$*" >&2; failures=$((failures + 1)); }
step_ok()   { printf '[check-ci] ok:   %s\n' "$*"; }
step_skip() { printf '[check-ci] skip: %s\n' "$*"; }

need_uv() {
  if ! command -v uv >/dev/null; then
    printf '[check-ci] ERROR: uv not on PATH; run .agents/bootstrap.sh first\n' >&2
    exit 2
  fi
}

run_sphinx() {
  need_uv
  local d
  for d in "${SPHINX_DIRS[@]}"; do
    if [[ ! -f "${d}/conf.py" ]]; then
      step_skip "sphinx ${d} (no conf.py)"
      continue
    fi
    # -W: warnings are errors (matches the strictness a reviewer wants; CI's
    #     `make html` does not set -W but the reviewer's ratchet is stricter
    #     than CI's minimum).
    # -n: nit-picky; catches unresolved :ref:/:term:/:doc: references.
    # -q: quiet; a failing build still prints the offending file+line.
    if uv run sphinx-build -W -n -q -b html "${d}" "${d}/_build/html" 2>&1 \
        | sed "s|^|[${d}] |"; then
      step_ok "sphinx ${d}"
    else
      step_fail "sphinx ${d} (see output above)"
    fi
  done
}

ensure_lychee() {
  if command -v lychee >/dev/null; then return 0; fi
  # lychee ships pre-built binaries; try the installer script from the
  # lycheeverse project. If the network is unavailable, fail loudly rather
  # than silently skipping -- an absent link check is worse than a slow one.
  printf '[check-ci] installing lychee (matches lycheeverse/lychee-action)\n'
  if command -v cargo >/dev/null; then
    cargo install lychee --locked >/dev/null 2>&1 || return 1
  else
    curl -sSfL https://raw.githubusercontent.com/lycheeverse/lychee/master/install.sh \
      | bash -s -- -b "${HOME}/.local/bin" >/dev/null 2>&1 || return 1
    export PATH="${HOME}/.local/bin:${PATH}"
  fi
  command -v lychee >/dev/null
}

run_links() {
  if ! ensure_lychee; then
    step_fail "lychee unavailable; install manually (see lycheeverse/lychee README)"
    return
  fi
  if lychee "${LYCHEE_ARGS[@]}" "${LYCHEE_GLOBS[@]}"; then
    step_ok "lychee"
  else
    step_fail "lychee (broken or unreachable links; see output above)"
  fi
}

case "${1:-all}" in
  sphinx) run_sphinx ;;
  links)  run_links ;;
  all)    run_sphinx; run_links ;;
  *)      printf 'usage: %s [sphinx|links|all]\n' "$0" >&2; exit 2 ;;
esac

if ((failures)); then
  printf '[check-ci] %d check(s) failed\n' "${failures}" >&2
  exit 1
fi
printf '[check-ci] all checks passed\n'
