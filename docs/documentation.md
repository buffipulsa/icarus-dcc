# Documentation publishing

The documentation is built from the guides in `docs/` and the Python
docstrings in `src/icarus_dcc/`.

GitHub Actions checks documentation on pull requests to `main`. Successful
builds on `main` are automatically published to
[GitHub Pages](https://buffipulsa.github.io/icarus-dcc/).
Feature branch changes become public after they are merged into `main`.

## Local preview

From the repository root, run:

```powershell
uv run --no-project --python 3.10 --with-requirements docs/requirements.txt sphinx-build -b html -W --keep-going docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser. Generated files are ignored
by Git. The documentation dependencies are separate from the development
environment, so this also works without Maya or Qt installed.

## Updating content

- Edit the Markdown guides directly.
- Write API docstrings in NumPy style; Sphinx includes them automatically
  for the modules listed in `api.rst`.
- Add new guide pages to the `toctree` in `index.rst`.
- Add new public modules to `api.rst` when they are ready to document.

Warnings fail the build, and failed builds leave the last published site
in place. The workflow can also be run manually from GitHub Actions.

Maya imports are mocked only during documentation builds. Examples are
displayed rather than executed, so a successful build is not a Maya test.
