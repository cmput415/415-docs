# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'generator'
copyright = '2023, cmput415'
author = 'cmput415'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
]

# Cross-reference the Gazprea glossary.  The tuple's first element is the
# canonical URL used to rewrite resolved refs; the second element is a list
# of inventory-source fallbacks.  ``../gazprea/_build/html/objects.inv``
# resolves against this file's directory, so ``make all`` (which builds
# gazprea first per the top-level Makefile) always finds the inventory
# locally.  If the local file is missing, intersphinx falls back to the
# published URL and the build still succeeds.
intersphinx_mapping = {
    'gazprea': (
        'https://cmput415.github.io/415-docs/gazprea',
        ('../gazprea/_build/html/objects.inv', None),
    ),
}

# Never let a bare :doc:`foo` silently resolve to a sibling project's page;
# force ``:external+gazprea:doc:`` when that is actually what is meant.
intersphinx_disabled_reftypes = ['std:doc']

# Toggles the display of "Todo" message boxes in the output
todo_include_todos = True

# Toggle warnings in build log when todos are present
todo_emit_warnings = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'style_nav_header_background': '#007C41',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': False,
}

html_logo = 'assets/images/logo-reverse.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/googleFonts.css',
]

# Disable syntax highlighting in code blocks
highlight_language ='none'


# -- Options for linkcheck ---------------------------------------------------
#
# Stack Exchange sites 403 unauthenticated linkcheckers even though the
# pages are visible in a browser.  Verified in-browser on 2026-08-03.
linkcheck_ignore = [
    r'^https?://([a-z]+\.)?stackexchange\.com/',
    r'^https?://([a-z]+\.)?stackoverflow\.com/',
]
linkcheck_anchors = False
linkcheck_timeout = 30
linkcheck_retries = 2
