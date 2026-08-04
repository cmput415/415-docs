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
PYTHON                ?= python3

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile canvas

# ``canvas`` is always run (no file-target prerequisites) so we don't
# collide with the ``%: Makefile`` catch-all below, which would otherwise
# try to sphinx-build any explicit source-file prerequisite we listed.
canvas:
	@mkdir -p $(dir $(CANVAS_GLOSSARY_OUT))
	$(PYTHON) $(CANVAS_GLOSSARY_TOOL) \
	    --input $(CANVAS_GLOSSARY_SRC) \
	    --output $(CANVAS_GLOSSARY_OUT)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
