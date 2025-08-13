# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Find source tree for python

import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../HammerSDK/'))

# -- Project information -----------------------------------------------------

project = 'HammerSDK'
copyright = '2023, Hammerspace'
author = 'Michael Kade'
version = '1.0.0'
release = '1.0.0'
language = 'en'

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- API Documentation

autoapi_dirs = ["../HammerSDK/"]
autoapi_options = ["members", "show-inheritance", "show-module-summary", "imported-members"]


# -- API Excludes

def skip_util_classes(app, what, name, obj, skip, options):
    skip = False

    # Don't doc the HammerSDK.lib package

    if what == "package" and "HammerSDK.lib" in name:
        skip = True

    # Don't doc the classes in HammerSDK.rest.objectives

    elif what == "class" and "HammerSDK.rest.objectives" in name:
        skip = True

    # Don't output private members
    
    elif what == "function":
        if "HammerSDK.rest.objectives._" in name or \
           "HammerSDK.rest.shares._" in name or \
           "HammerSDK.rest.nodes._" in name or \
           "HammerSDK.rest.logical_volumes._" in name or \
           "HammerSDK.rest.share_snapshots._" in name or \
           "HammerSDK.rest.volume_groups._" in name:
            skip = True
        
    # Don't doc any attribute, function, or property in the HammerSDK.hammer_client

    elif "HammerSDK.hammer_client" in name:
        if what == "attribute" or \
           what == "function" or \
           what == "property":
            skip = True

        # Skip certain methods in the HammerClient

        if what == "method":
            if name == "HammerSDK.hammer_client.HammerClient.__init__":
                skip = True
            elif name == "HammerSDK.hammer_client.HammerClient.close":
                skip = True
            elif name == "HammerSDK.hammer_client.HammerClient.request":
                skip = True
    
    if not skip:
        print(f"What: {what}, Name: {name}")

    return skip


# Setup and run sphinx doc build

def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_util_classes)
