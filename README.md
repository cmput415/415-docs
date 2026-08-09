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
sessions over the spec. The three shell scripts (`bootstrap.sh`, `check.sh`,
`healthcheck.sh`) are **rendered from `.agents/*.tmpl` and are not committed
-- regenerate them at the start of each session:

    for t in .agents/*.tmpl; do
      uv run .agents/render.py .agents/manifest.yaml "$t" > "${t%.tmpl}"
      chmod +x "${t%.tmpl}"
    done
    .agents/bootstrap.sh
    [[ -r .agents/agent-env.sh ]] && source .agents/agent-env.sh

`bootstrap.sh` installs system packages, installs `uv` if missing, runs
`uv sync` to provision the Python venv from `pyproject.toml`, and records
baselines that `healthcheck.sh` compares the live environment against.

**Commit signing is opt-in.** The `agent:` block in `manifest.yaml` is
blank by default; bootstrap only mints a GPG signing key when you fill it
in with a name and email. Filling it in is a per-user choice -- treat the
blank template as the shared committed state and keep your populated copy
local. When you do configure signing, register the exported public key
(`gpg --homedir .agents/gnupg --armor --export <fpr>`) on the forge before
your first push.

Bundled skills for spec review/consistency work live under
`.agents/skills/` and are listed in `manifest.yaml`'s `skills:`. The
healthcheck confirms each listed skill still has a non-empty `SKILL.md`.
