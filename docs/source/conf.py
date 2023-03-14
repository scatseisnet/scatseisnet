import os
import sys

# Path setup
sys.path.insert(0, os.path.abspath("../../"))

# Project information
project = "scatseisnet"
copyright = "2021, Léonard Seydoux and René Steinmann"
author = "Léonard Seydoux and René Steinmann"

release = "0.2.0"
version = "0.2.0"

# General configuration
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
]

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_gallery.load_style",
    "sphinx_favicon",
    "sphinx_design",
    "autoapi.extension",
    "nbsphinx",
    "numpydoc",
    "IPython.sphinxext.ipython_console_highlighting",
]

favicons = [
    "logo_scatseisnet_notext.png",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("http://docs.scipy.org/doc/numpy/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

intersphinx_disabled_domains = [
    "std",
]

templates_path = [
    "_templates",
]

# Options for HTML output

html_theme = "pydata_sphinx_theme"

html_static_path = [
    "_static",
]

html_theme_options = {
    "pygment_light_style": "tango",
    "pygment_dark_style": "monokai",
    "github_url": "https://github.com//scatseisnet/scatseisnet",
    "announcement": "This is a beta release of the scatseisnet package. Please report any issues you find <a href=https://github.com/scatseisnet/scatseisnet/issues>in the GitHub repository</a>.",
}

html_context = {
    "github_repo": "https://github.com/scatseisnet/scatseisnet",
}


# Options for AutoAPI
autoapi_type = "python"
autoapi_dirs = ["../../scatseisnet"]
autosummary_generate = True

# Theme options are theme-specific and customize the look and feel of a theme
# further. For a list of options available for each theme, see the
# documentation.
html_logo = "_static/logo_scatseisnet_notext.png"

# Language
language = "en"
