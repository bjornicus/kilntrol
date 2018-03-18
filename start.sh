#!/bin/sh
echo starting kilntrol
python3 kilntrol.py &

sleep 1
echo starting log uploader
python upload_logs.py &

echo started processes: 
jobs -p

# this will kill the started processes
# trap 'kill $(jobs -p)' EXIT