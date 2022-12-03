#!/bin/bash

hugo --cleanDestinationDir --minify
rsync -avz --delete public/ sw:./new

exit 0
