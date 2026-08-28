# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Canvas-ready standalone HTML glossary.  Runs a dependency-free Python
# converter over spec/glossary.rst and drops the result in
# _build/canvas/gazprea-glossary.html so it can be pasted into Canvas
# or copied into the GH-Pages site by the top-level Makefile.
CANVAS_GLOSSARY_SRC   := spec/glossary.rst
CANVAS_GLOSSARY_OUT   := $(BUILDDIR)/canvas/gazprea-glossary.html
CANVAS_GLOSSARY_TOOL  := _ext/build_canvas_glossary.py
# Base URL (repo root) + Sphinx inventory ($(BUILDDIR)/html/objects.inv,
# produced by ``make html``) let the converter resolve :ref: cross-references
# to live links on the published site.
CANVAS_GLOSSARY_BASEURL := ../.baseurl
CANVAS_GLOSSARY_INV     := $(BUILDDIR)/html/objects.inv

# Tangled example tests.  Scans the RST sources for gazprea-example(-wrap)
# directives and packages one .gaz lit test per example into a .tar.gz that
# drops into the solution compiler's tests/ tree.  Dependency-free, like the
# Canvas converter above; not part of the rendered spec.
EXAMPLES_OUT   := $(BUILDDIR)/examples/gazprea-examples.tar.gz
EXAMPLES_TOOL  := _ext/tangle_examples.py

PYTHON                ?= python3

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile canvas examples

# ``canvas`` is always run (no file-target prerequisites) so we don't
# collide with the ``%: Makefile`` catch-all below, which would otherwise
# try to sphinx-build any explicit source-file prerequisite we listed.
canvas:
	@mkdir -p $(dir $(CANVAS_GLOSSARY_OUT))
	$(PYTHON) $(CANVAS_GLOSSARY_TOOL) \
	    --input $(CANVAS_GLOSSARY_SRC) \
	    --output $(CANVAS_GLOSSARY_OUT) \
	    --baseurl-file $(CANVAS_GLOSSARY_BASEURL) \
	    --inventory $(CANVAS_GLOSSARY_INV)

# ``examples`` tangles the gazprea-example(-wrap) blocks into a .tar.gz of
# lit tests.  Same rationale as ``canvas`` for being phony.
examples:
	@mkdir -p $(dir $(EXAMPLES_OUT))
	$(PYTHON) $(EXAMPLES_TOOL) \
	    --source . \
	    --output $(EXAMPLES_OUT)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
