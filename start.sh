#!/bin/sh

# SIGTERM-handler
term_handler() {
    jobs -l
    [[ -n "$kilntrol_pid" ]] && echo stoping kilntrol && kill $kilntrol_pid
    [[ -n "$upload_pid" ]] &&  echo stopping log upload && kill $upload_pid
    [[ -n "$sim_pid" ]] &&  echo stopping heater sim && kill $sim_pid

    exit 0
}
trap 'term_handler' EXIT

if [ $1 = "sim" ]
then
    echo starting heater simulator
    python3 src/heater_sim.py &
    sim_pid=$!
fi

echo starting log uploader
python src/upload_logs.py &
upload_pid=$!

echo starting kilntrol
python3 src/kilntrol.py $1
