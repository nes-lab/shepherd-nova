# Configuration file for the Sphinx documentation builder.
#
# -- Project information -----------------------------------------------------

project = "Shepherd Nova"
project_full = "Public Instance of the Shepherd Testbed"
copyright = "2025, NES Lab, TU Darmstadt & TU Dresden"
author = "Ingmar Splitt"
release = "0.6.0"
builder = "html"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx_sitemap",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Extension configuration ---------------------------------------------- --
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

myst_enable_extensions = [
    "colon_fence",  # also allow ::: in addition to ```-blocks & admonitions
    "replacements",  # converts +- (and more) to a single character
    # "dollarmath",
    "tasklist",
]
myst_heading_anchors = 3  # call via [**link text**](./file.md#headings)

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinxawesome_theme"

html_theme_options = {
    "show_scrolltop": True,
    "show_breadcrumbs": True,
    "show_prev_next": True,
    "logo_light": "media/nes_logo.svg",
    "logo_dark": "media/nes_logo.svg",
    "awesome_external_links": True,
    # "extra_header_link_icons": {"media/TUD_Logo.svg": "https://cfaed.tu-dresden.de/"},# WRONG
    # "main_nav_links": {"About": "/content/about"},
    # "max_navbar_depth": 2,
    # "show_nav_level": 2,
    # "navigation_depth": 2,
}
# https://sphinxawesome.xyz/how-to/options/

# Select a color scheme for light mode
pygments_style = "friendly"
# Select a different color scheme for dark mode
# pygments_style_dark = "friendly"
# see https://pygments.org/styles/ for more

html_title = project

html_baseurl = "https://nes-lab.github.io/shepherd-nova/"
html_permalinks_icon = "<span>#</span>"
html_static_path = ["_static"]
html_extra_path = ["robots.txt"]

sitemap_url_scheme = "{link}"
