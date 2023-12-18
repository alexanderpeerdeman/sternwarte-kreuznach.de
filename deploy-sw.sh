#!/usr/bin/env bash

hugo --cleanDestinationDir --minify
rsync -avz --delete public/ sw:./new