#!/bin/bash

# Clean out the docs directory

cd docs
make clean
cd ..

# Build a virtual environment before we build the library. That way, we can
# test all of the functionality

rm -rf .venv

pip3 cache purge

python3 -m venv .venv
source .venv/bin/activate

# Install needed packages

pip install --upgrade pip
pip install tbump
pip install build
pip install flake8
pip install sphinx
pip install pydata_sphinx_theme
pip install sphinx_rtd_theme
pip install sphinx-autoapi

# Build the HammerSDK library and install it

cd HammerSDK
rm -rf dist *.egg-info
python -m build
pip install .

# Build the documentation

cd ..
cd docs
make clean
sphinx-build -b html . _build
