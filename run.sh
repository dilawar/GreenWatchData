#!/usr/bin/env bash
set -x
set -e
for state in 'Andhra Pradesh' 'Telangana' 'Karanataka' \
    'Rajasthan' 'Gujarat' 'Maharashtra' 'Madhya Pradesh' \
    'Tamil Nadu'; do
    python3 ./download_all_kml_selenium.py $state 'CA Land'
done
