# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Template variables for easy customization ------------------------------
PROJECT_NAME = "[PROJECT_NAME]"
PROJECT_REPO = "[PROJECT_REPO]"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = PROJECT_NAME
copyright = "2025, SplendidCube"
author = "SplendidCube"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_wagtail_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_wagtail_theme"
html_static_path = ["_static"]

# Custom CSS files (loaded after theme CSS)
html_css_files = [
    "custom.css",
]

# -- MyST configuration ------------------------------------------------------
# Enable MyST Markdown parser
source_suffix = {
    ".rst": None,
    ".md": "markdown",
}

# MyST configuration
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_admonition",
    "html_image",
]

# -- Custom configuration ---------------------------------------------------
html_title = PROJECT_NAME
html_short_title = PROJECT_NAME
html_logo = None
html_favicon = None

# Theme options
html_theme_options = {
    "project_name": PROJECT_NAME,
    "logo": "logo.svg",  # SVG logo for crisp scaling
    "logo_alt": "SplendidCube Logo",
    "logo_height": 60,   # Slightly larger to accommodate the cube design
    "logo_url": "/",
    "logo_width": 56,    # Maintains aspect ratio (522.69/560.21 ≈ 0.93)
    # "github_url": f"https://github.com/SplendidCube/{PROJECT_REPO}",  # Commented out to hide Edit button
}
