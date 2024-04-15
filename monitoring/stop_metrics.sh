#!/bin/bash
if [ ! -f ".pid" ]; then
    echo "Metrics service not running"
    exit 1
fi
PID=$(cat .pid)
kill $PID
rm .pid
echo "Metrics service stopped"