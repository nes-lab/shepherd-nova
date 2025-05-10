# Shepherd Nova

[![QA-Tests](https://github.com/nes-lab/Shepherd-Nova/actions/workflows/quality_assurance.yaml/badge.svg)](https://github.com/nes-lab/Shepherd-Nova/actions/workflows/quality_assurance.yaml)
[![Documentation](https://github.com/nes-lab/Shepherd-Nova/actions/workflows/pages_update.yaml/badge.svg)](https://nes-lab.github.io/Shepherd-Nova/)
[![PyPiVersion](https://img.shields.io/pypi/v/shepherd_data.svg)](https://pypi.org/project/shepherd_data)

This Repo contains the documentation for the public instance of the Shepherd Testbed.

The documentation is compiled with [Sphinx](https://www.sphinx-doc.org/) and uses the [MyST-extension](https://myst-parser.readthedocs.io/en/latest/index.html) to allow embedding Markdown-files.

## Get sources and dependencies

Example-workflow using `git` and `pip`.

```Shell
git clone https://github.com/nes-lab/Shepherd-Nova
cd Shepherd-Nova
pip install .
```

## Generate Docs

Sphinx is used to build the website.

```Shell
sphinx-build -b html ./docs ./docs/_build/html
```

Viewing the document in a browser:

```Shell
cd ./docs/_build/html
python -m http.server
```

In browser go to <localhost:8000> to view the documentation.
