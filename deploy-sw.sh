#!/bin/bash

hugo
rsync -avz --delete public/ sw:./new

exit 0