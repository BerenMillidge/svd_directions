#!/bin/bash
pip install -r requirements.txt --user

# setup pysvelte for visualization:
# we use this fork from tomfrederik to enable pip installation:
git clone https://github.com/TomFrederik/PySvelte.git

# copy our visualization code from the repo to pysvelte:
cp -r visualization/* PySvelte/src/

cd PySvelte
pip install -e .
cd ..