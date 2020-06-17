#!/bin/bash
# Script to load data for selected organism

organism=(${ORGANISM//|/ })
assembly=(${ASSEMBLY//|/ })

for key in "${!organism[@]}"; do echo "$key ${organism[$key]}"; done

for key in "${!organism[@]}"
do
    python3 /var/www/html/src/setup/setup.py -r /var/www/html -g ${organism[$key]} -v ${assembly[$key]} -fa2bit \
    /var/www/html/bin/faToTwoBit -b /var/www/html/bin/ncbi-blast-2.7.1+/bin \
    && /var/www/html/src/setup/enable_dicey.sh ${organism[$key]} ${assembly[$key]}
done