#!/bin/bash

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# TODO: for mainnet need to change
# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   fullnode.devnet.sui.io" >> /etc/hosts
echo "127.0.0.1   api.openai.com" >> /etc/hosts

echo -e "y\n\n1" | sui client

python3.10 /app/traffic_forwarder.py 127.0.0.1 443 3 8002 &

cd /app || exit
python3.10 openai_call.py
# Start the server
python3.10 server.py