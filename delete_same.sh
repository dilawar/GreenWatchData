#!/usr/bin/env bash
for dir in $(find . -mindepth 2 -type d); do
    if [[ ! "$dir" = *".git"* ]]; then
        (
            cd $dir;
            fdupes -r -d -N .
        )
    fi
done
