#!/bin/bash

rm -r public
hugo --cleanDestinationDir --minify
rsync -avz --delete public/* sw:./new