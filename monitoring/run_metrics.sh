#!/bin/bash
if [ -f ".pid" ]; then
    echo "Metrics service already running"
    exit 1
fi
nohup uvicorn metrics:app --host 0.0.0.0 --port 9101 &
echo $! > .pid
echo "Metrics service started"