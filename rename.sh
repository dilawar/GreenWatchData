#!/usr/bin/env bash

# IFS="\n"
for file in $(find . -type f -name "*.kml" -print0); 
do
    mv "$file" "${file//[[:space:]]}"
done
