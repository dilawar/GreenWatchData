#!/usr/bin/env bash
set -x
set -e
for catype in 'CA Land' 'Diverted Land'; do
    for state in 'Andhra Pradesh' 'Telangana' 'Karanataka' \
        'Rajasthan' 'Gujarat' 'Maharashtra' 'Madhya Pradesh' \
        'Tamil Nadu'; do
        python3 ./download_all_kml_selenium.py "$state" "$catype"
    done
done
