# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

# Step 1 - If you don't have the base r.st files, you'll need to generate the stubs
# with a CMD call to sphinx-apidoc.
# You'll need two calls as this needs to be done for the common library too.

"""
sphinx-apidoc -f -o source '../playblast_plus' 
sphinx-apidoc -f -o source '../playblast_plus/hosts/maya'  
"""

# IMPORTANT!!!!
# you need to add every path that a module resides on for sphinx to detect it. 
# we are needing to jump back 2 directories, hence why we have ../../

# To build from CMD
# ./make clean - clears the build directory
# ./make html - builds the html site

sys.path.insert(0, os.path.abspath('..'))

project = 'Playblast Plus'
copyright = '2023, Pete Addington'
author = 'Pete Addington'

# The full version, including alpha/beta/rc tags
release = '1.2'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# 'sphinx.ext.coverage',

sys.path.append(os.path.abspath('../exts'))
extensions = [
                'sphinx.ext.autodoc', 
                'sphinx.ext.napoleon',
                'sphinx.ext.autosummary',
                'sphinx.ext.autosectionlabel',
                'sphinx.ext.githubpages'
            ]

napoleon_google_docstring = True


# IMPORTANT!!!!
# you need to create exceptions for maya specific classes, otherwise the build will grumble and fail

# autodoc_mock_imports
# This value contains a list of modules to be mocked up. This is useful when some external dependencies are not met at build time and break the building process. You may only specify the root package of the dependencies themselves and omit the sub-modules:

# autodoc_mock_imports = ["django"]
# Will mock all imports under the django package.

autodoc_mock_imports = ['vendor.Qt','pymel.core', 'maya.cmds', 'maya.mel','pymel', 'PySide2', 'maya', 'shiboken2','urllib2','long','int', 'pymxs.runtime']
# autosummary_generate = True  # Turn on sphinx.ext.autosummary

# autodoc_default_options = {
#     'show-inheritance': False,
#     'members': True,
#     'member-order': 'bysource',
#     'special-members': '__init__',
#     'undoc-members': True,
#     'exclude-members': '__weakref__'
# }
# autoclass_content = 'both'

html_logo = "images/thelinelogo.png"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

if html_theme == "sphinx_rtd_theme":
    html_css_files = ["css/theme_overrides.css"]

html_sidebars = {'**': ['fulltoc.html']}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'globaltoc_depth': 4,
    'globaltoc_collapse': 4,
}