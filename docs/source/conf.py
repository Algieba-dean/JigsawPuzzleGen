import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "JigsawPuzzle"
copyright = "2024"
author = "Your Name"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# 添加对 markdown 文件的支持
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
