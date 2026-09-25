"""Build the documentation without installing Maya or Qt."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

project = 'Icarus DCC'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'myst_parser',
]

autodoc_mock_imports = [
    'maya'
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

exclude_patterns = [
    '_build'
]

html_theme = 'alabaster'
html_title = 'Icarus DCC'
html_baseurl = 'https://buffipulsa.github.io/icarus-dcc/'
html_theme_options = {
    'github_user': 'buffipulsa',
    'github_repo': 'icarus-dcc',
    'github_button': True,
}
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
