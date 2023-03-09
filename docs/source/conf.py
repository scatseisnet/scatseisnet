# Configuration file for the Sphinx documentation builder.

import os
import sys

# Path setup
sys.path.insert(0, os.path.abspath("../../"))

# Project information

project = "scatseisnet"
copyright = "2021, The scatseisnet developers"
author = "Léonard Seydoux and René Steinmann"

release = "0.1"
version = "0.1.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "nbsphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "pydata_sphinx_theme"

# html_theme_options = {
#     "logo_only": True,
#     "style_nav_header_background": "#fcf4d2",
# }

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_logo = "_static/logo_scatseisnet_notext.png"

# -- Options for EPUB output
epub_show_urls = "footnote"
