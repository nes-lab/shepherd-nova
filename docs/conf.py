# Configuration file for the Sphinx documentation builder.
#
# -- Project information -----------------------------------------------------

project = 'Shepherd Nova'
project_full = "Public Instance of the Shepherd Testbed"
copyright = '2025, Ingmar Splitt'
author = 'Ingmar Splitt'
release = '0.1.0'
builder = "html"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinxawesome_theme",
    "sphinx_sitemap",
    "myst_parser",
]

templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinxawesome_theme'

html_theme_options = {
    "show_scrolltop": True,
    "show_prev_next": True,
#    "main_nav_links": {
#    },
}
# TODO: https://sphinxawesome.xyz/how-to/options/

html_baseurl = "https://nes-lab.github.io/Shepherd-Nova/"
html_permalinks_icon = "<span>#</span>"
html_static_path = ['_static']
html_extra_path = ["robots.txt"]

sitemap_url_scheme = "{link}"
