#!/bin/bash

rm -r public
hugo --cleanDestinationDir --minify
rsync -avz --delete public/* uberspace:./html