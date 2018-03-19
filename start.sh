#!/bin/sh
echo starting kilntrol
python3 kilntrol.py | tee logs/kilntrol.log &

sleep 1
echo starting log uploader
python upload_logs.py | tee logs/upload.log &

echo started processes: 
jobs -p

# this will kill the started processes
# trap 'kill $(jobs -p)' EXIT