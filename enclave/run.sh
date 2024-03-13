#!/bin/bash

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   api.openai.com" >> /etc/hosts
echo "127.0.0.1   google.serper.dev" >> /etc/hosts
echo "127.0.0.1   testnet.galadriel.com" >> /etc/hosts

python3.10 /app/traffic_forwarder.py 127.0.0.1 443 &

# sleep so there is time to open enclave debug logs before the server potentially crashes
sleep 10
# python3.10 /app/check_proxies.py

# Start the server
python3.10 /app/server.py &

sleep 30
python3.10 /app/key_manager.py

# TODO: remove these for production!
echo "DOT ENV"
cat /app/.env
echo "\nGCP CREDENTIALS"
cat /app/sidekik.json

echo "Pinging for funds"
cd /app && python3.10 oracle_ping_for_funds.py

# Start oracle setup
echo "Starting the oracle!"
tail -f /dev/null
