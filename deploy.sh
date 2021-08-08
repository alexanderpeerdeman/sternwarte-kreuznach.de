#!/bin/bash

rm -r public
hugo --cleanDestinationDir --minify
rsync -aP --delete public/* uberspace:./html
xdg-open "https://apeer.uber.space"