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

html_theme = 'furo'
html_title = 'Icarus DCC'
html_baseurl = 'https://buffipulsa.github.io/icarus-dcc/'
html_theme_options = {
    'source_repository': 'https://github.com/buffipulsa/icarus-dcc/',
    'source_branch': 'main',
    'source_directory': 'docs/',
}
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
