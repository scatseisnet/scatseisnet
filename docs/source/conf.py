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

# Add redirect for RTD using Sphinx setup function
def setup(app):
    if os.environ.get("READTHEDOCS") == "True":
        # Add meta tags to block search engines
        app.add_css_file(None, content="""
            body::before {
                content: "📍 Documentation Has Moved! This site is no longer maintained. You will be redirected to https://scatseisnet.github.io/scatseisnet/ in 3 seconds.";
                display: block;
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                padding: 20px;
                margin: 20px;
                text-align: center;
                font-family: Arial, sans-serif;
                color: #856404;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        # Add redirect script
        redirect_script = """
        document.addEventListener('DOMContentLoaded', function() {
            var meta = document.createElement('meta');
            meta.name = 'robots';
            meta.content = 'noindex, nofollow';
            document.head.appendChild(meta);
            
            setTimeout(function() {
                var currentPath = window.location.pathname.replace('/en/latest/', '/').replace('/en/stable/', '/');
                var newUrl = 'https://scatseisnet.github.io/scatseisnet' + currentPath;
                window.location.href = newUrl;
            }, 3000);
        });
        """
        app.add_js_file(None, body=redirect_script)


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
