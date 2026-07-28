# Editing the Spec

This project uses [Sphinx](https://www.sphinx-doc.org/) to generate
documentation from [reStructuredText](https://docutils.sourceforge.io/rst.html)
(RST).

For a quick introduction to Sphinx, refer to the
[Sphinx Quickstart](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
documentation.

For a quick introduction to RST, refer to the
[reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).

# Building

## Required Software
- `texlive-full` (for PDF output only)
- `python`

## Required Python (PyPI) Packages
- `sphinx`
- `sphinx_rtd_theme`

## Usage

- `make html` to build html files
- `make latexpdf` to build PDF/LaTeX files
- `make clean` to delete build files

The HTML build is output to the `_build/html` folder.  
The PDF/LaTeX build is output to the `_build/latex` folder.
