#!/bin/bash

FILES="*.png *.svg *.html *.mjs *.js *.json *.celer *.css leaflet codemirror node_modules"

rsync -arvz $FILES restite.org:html/notceler-totk

echo "https://restite.org/notceler-totk"

