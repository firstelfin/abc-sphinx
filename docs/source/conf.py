# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = 'abc-sphinx'
copyright = '2025, elfin'
author = 'elfin'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../../abc-sphinx/'))

extensions = [
    'abcSphinx',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

abc_force_rebuild = True 

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# html_extra_path = ['_abc_images']  # 配置项

abc_global_classes = ["music-sheet", "responsive"]
