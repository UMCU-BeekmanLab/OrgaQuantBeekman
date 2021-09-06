#!/bin/bash
source OrgaQuant/bin/activate
for dir in data/*/
do
    python scripts/batchDetection.py $dir 2> $dir/error.log 1> $dir/info.log
done