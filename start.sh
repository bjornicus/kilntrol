#!/bin/sh

# SIGTERM-handler
term_handler() {
    [[ -n "$kilntrol_pid" ]] && kill $kilntrol_pid
    [[ -n "$upload_pid" ]] && kill $upload_pid

    exit 0
}
trap 'term_handler' INT QUIT TERM EXIT

echo starting kilntrol
python3 src/kilntrol.py | tee logs/kilntrol.log &
kilntrol_pid=$!

sleep 1
echo starting log uploader
python src/upload_logs.py | tee logs/upload.log &
upload_pid=$!

# wait "indefinitely"
while [[ -e /proc/$kilntrol_pid ]]; do
    wait $kilntrol_pid # Wait for any signals or end of execution of kilntrol
done

# Stop container properly
term_handler