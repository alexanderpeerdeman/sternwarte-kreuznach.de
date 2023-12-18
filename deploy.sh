#!/usr/bin/env bash
 
hugo --cleanDestinationDir --minify
rsync -avz --delete public/* uberspace:./html