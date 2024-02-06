import sys
import os


project = 'TextSynth Python Interface'
copyright = '2024, Christopher Ptak'
author = 'Christopher Ptak'
release = '0.1'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme'
]

autoclass_content = 'both'
autodoc_typehints = 'description'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

