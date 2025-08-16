# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add paths for module autodiscovery
sys.path.insert(0, os.path.abspath(".."))

# -- Template variables for easy customization ------------------------------
PROJECT_NAME = "ansible.role.prep"
PROJECT_REPO = f"https://github.com/SplendidCube/{PROJECT_NAME}"

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
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_wagtail_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Exclude test fixtures and problematic modules from autodoc
autodoc_mock_imports = [
    "ansible",
    "ansible.module_utils",
    "ansible.module_utils.basic",
    "troposphere",
    "stringcase",
    "pytest",
    "grappa",
    "pepper8",
]

# Skip importing test fixtures to avoid execution
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"]
autodoc_member_order = "bysource"

# -- Autodoc configuration --------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Generate autosummary stub pages
autosummary_generate = True
autosummary_imported_members = True

# Napoleon settings for Google/NumPy docstring parsing
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx mapping for external documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "ansible": ("https://docs.ansible.com/ansible/latest/", None),
}

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
    "logo_height": 60,  # Slightly larger to accommodate the cube design
    "logo_url": "/",
    "logo_width": 56,  # Maintains aspect ratio (522.69/560.21 ≈ 0.93)
    "github_url": PROJECT_REPO,  # GitHub repository URL for Edit button
}
