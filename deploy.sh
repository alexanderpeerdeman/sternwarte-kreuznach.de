#!/bin/bash

rm -r public
#hugo
hugo --cleanDestinationDir --minify
rsync -aP --delete public/* uberspace:./html