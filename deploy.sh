#!/bin/bash

rm -r public
#hugo
hugo --cleanDestinationDir --minify
source venv/bin/activate
python create_search_index.py
rsync -aP --delete public/* uberspace:./html

deactivate
