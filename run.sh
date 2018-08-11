#!/usr/bin/env bash
set -x
set -e
for catype in 'CA Land' 'Diverted Land'; do
    for state in 'Andhra Pradesh' 'Telangana' 'Karnataka' \
        'Rajasthan' 'Gujarat' 'Maharashtra' 'Madhya Pradesh' \
        'Tamil Nadu'; do
        python3 ./download_all_kml_selenium.py "$state" "$catype"
    done
done
find . -type f -name "*.kml" > ./list_of_files.md
fdupes -r -q . > ./duplicates.md
