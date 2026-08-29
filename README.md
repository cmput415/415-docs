# 415-docs
This repository holds all of the documentation for CMPUT 415.

The files are served from https://cmput415.github.io/415-docs.

The site is automatically updated using a Github Action when
  1. a commit is pushed to the master branch
  3. the action is manually triggered from the Github Actions page

For more details on the Github Action workflow, see
`.github/workflows/deploySite.yml`

## Agent sessions

The `.agents/` scaffold is opt-in tooling for reproducible agent-run review
sessions over the spec.

### Docker (preferred)

The [`ghcr.io/cmput415/docs-dev`](https://github.com/cmput415/ci-utils)
image bundles the toolchain the review session needs (Sphinx + latexmk +
texlive, `lychee`, `uv`, [`act`](https://github.com/nektos/act) for
replaying the repo's GitHub Actions locally, and `gnupg` + `graphviz`).
Bump the tag reference in `.agents/manifest.yaml` when the ci-utils image
is rebuilt; keep this README in sync.

    docker run --rm -it -v "$PWD":/workspace \
      ghcr.io/cmput415/docs-dev:latest bash

Inside the container you can go straight to `uv sync && make -C gazprea
html` or `act -j build` without any host apt work.

### Native (fallback)

If you cannot use the image, render the three shell helpers from their
templates and run bootstrap. The rendered scripts are **not committed** --
regenerate them at the start of each session:

    for t in .agents/*.tmpl; do
      uv run .agents/render.py .agents/manifest.yaml "$t" > "${t%.tmpl}"
      chmod +x "${t%.tmpl}"
    done
    .agents/bootstrap.sh
    [[ -r .agents/agent-env.sh ]] && source .agents/agent-env.sh

`bootstrap.sh` installs system packages, installs `uv` if missing, runs
`uv sync` to provision the Python venv from `pyproject.toml`, and records
baselines that `healthcheck.sh` compares the live environment against.

### Identity

Commit signing is opt-in and not prescribed by this repo. The `agent:`
block in `manifest.yaml` is blank; bootstrap only mints a GPG signing key
when you fill in a name and email. Whether you sign, and under what
identity, is your call -- treat the blank template as the shared committed
state and keep any populated copy local. If you do configure signing,
register the exported public key
(`gpg --homedir .agents/gnupg --armor --export <fpr>`) on the forge before
your first push.

### Skills

Bundled skills for spec review/consistency work live under
`.agents/skills/` and are listed in `manifest.yaml`'s `skills:`. The
healthcheck confirms each listed skill still has a non-empty `SKILL.md`.
