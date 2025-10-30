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

# Copy robots.txt to the build output only on RTD (blocks search engine indexing)
# GitHub Pages won't include this file
if os.environ.get("READTHEDOCS") == "True":
    html_extra_path = [
        "robots.txt",
    ]

html_theme_options = {
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    "github_url": "https://github.com//scatseisnet/scatseisnet",
}

html_context = {
    "github_repo": "https://github.com/scatseisnet/scatseisnet",
}

# Add custom HTML for redirect on RTD
if os.environ.get("READTHEDOCS") == "True":
    html_theme_options.update({
        "announcement": """
        <div style="background-color: #fff3cd; border: 2px solid #ffc107; padding: 15px; text-align: center;">
        📍 <strong>Documentation Has Moved!</strong><br>
        This site is no longer maintained. Redirecting to 
        <a href="https://scatseisnet.github.io/scatseisnet/" style="color: #0066cc;">
        https://scatseisnet.github.io/scatseisnet/</a> in 3 seconds...
        </div>
        <script>
        setTimeout(function() {
            var currentPath = window.location.pathname.replace('/en/latest/', '/').replace('/en/stable/', '/');
            window.location.href = 'https://scatseisnet.github.io/scatseisnet' + currentPath;
        }, 3000);
        </script>
        <meta name="robots" content="noindex, nofollow">
        """
    })


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
