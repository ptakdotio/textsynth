import sys
import os


project = 'TextSynth Python Interface'
copyright = '2024, Christopher Ptak'
author = 'Christopher Ptak'
release = '0.1'


extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'alabaster'
html_static_path = ['_static']


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

