#!/bin/bash

rm -r public
hugo --cleanDestinationDir --minify
rsync -aP --delete public/* uberspace:./html