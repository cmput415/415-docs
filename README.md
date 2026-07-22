# 415-docs
This repository holds all of the documentation for CMPUT 415.

The files are served from https://cmput415.github.io/415-docs.

The site is automatically updated using a Github Action when
  1. a commit is pushed to the master branch
  3. the action is manually triggered from the Github Actions page

For more details on the Github Action workflow, see
`.github/workflows/deploySite.yml`

## Agent sessions

At the start of every agent session:

    .agents/healthcheck.sh && .agents/bootstrap.sh && source .agents/agent-env.sh

After changing `.agents/manifest.yaml`: re-render from the `.agents/*.tmpl`
templates (see `render.py`) and re-run bootstrap. A freshly minted agent key
(bootstrap logs "generating", not "reusing") must be re-registered on the
forge; the exported public key lives at `.agents/agent-pubkey.asc`.
