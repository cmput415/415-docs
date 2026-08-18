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

project = 'gazprea'
copyright = '2025, cmput415'
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

# Reserved for future back-references from Gazprea into sibling specs.
# The gazprea spec currently defines no :ref:/:term: targets pointing at
# a sibling, but wiring this symmetrically now means the first back-ref
# in a future edit will just work.  Same fallback pattern as the siblings:
# canonical URL plus local ``_build/html/objects.inv``.  When the top-level
# ``make all`` runs, siblings are built after gazprea, so a first ``make
# all`` from clean will fall back to the URL for these; a second run
# picks up the local files.
intersphinx_mapping = {
    'vcalc':     ('https://cmput415.github.io/415-docs/vcalc',
                  ('../vcalc/_build/html/objects.inv', None)),
    'scalc':     ('https://cmput415.github.io/415-docs/scalc',
                  ('../scalc/_build/html/objects.inv', None)),
    'setup':     ('https://cmput415.github.io/415-docs/setup',
                  ('../setup/_build/html/objects.inv', None)),
    'generator': ('https://cmput415.github.io/415-docs/generator',
                  ('../generator/_build/html/objects.inv', None)),
    'info':      ('https://cmput415.github.io/415-docs/info',
                  ('../info/_build/html/objects.inv', None)),
}

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

# Point the per-page source link at the file on GitHub rather than a local
# ``_sources/<page>.rst.txt`` copy: the deploy step strips ``_sources/``, so
# the default link 404s on the published site.  With these set, sphinx_rtd_theme
# renders a GitHub link built from
# ``<github_version><conf_py_path><pagename><suffix>``.
html_context = {
    'display_github': True,
    'github_user': 'cmput415',
    'github_repo': '415-docs',
    'github_version': 'master',
    'conf_py_path': '/gazprea/',
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
# URLs that a human can visit but a CI linkchecker cannot.  The pages exist;
# their servers block automated clients with 403 (or, for thewordfactory.com,
# quietly time them out).  Verified in-browser on 2026-08-03; if the ignore
# list ever hides a legitimate breakage, remove the entry and let CI fail.
linkcheck_ignore = [
    # ISO standards catalogue: every page 403s to non-browser user-agents.
    r'^https?://(www\.)?iso\.org/',
    # MDPI journals: 403 to bots.
    r'^https?://(dx\.)?doi\.org/10\.3390/',
    # ACM Digital Library (dl.acm.org, and DOI redirects to it): 403 to bots.
    r'^https?://(dx\.)?doi\.org/10\.1145/',
    r'^https?://dl\.acm\.org/',
    # cppreference.com: 403 to bots.
    r'^https?://en\.cppreference\.com/',
    # The Word Factory: connection times out to bots.
    r'^https?://(www\.)?thewordfactory\.com/',
]

# Give slow-responding but legitimate hosts more time before treating a
# response as a failure.
linkcheck_anchors = False
linkcheck_timeout = 30
linkcheck_retries = 2
