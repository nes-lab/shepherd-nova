# Shepherd Nova

[![QA-Tests](https://github.com/orgua/shepherd/actions/workflows/qc_tests.yml/badge.svg)](https://github.com/orgua/shepherd/actions/workflows/quality_assurance.yaml)
[![Documentation](https://github.com/orgua/shepherd/actions/workflows/sphinx_to_pages.yml/badge.svg)](https://nes-lab.github.io/shepherd-nova/)
[![PyPiVersion](https://img.shields.io/pypi/v/shepherd_herd.svg)](https://pypi.org/project/shepherd_data)

Public Instance of the Shepherd Testbed

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

In browser go to `<localhost:8000>`_ to view the documentation.
