#!/bin/bash

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Starting DNSMasq
echo "Starting DNSMasq..."
dnsmasq --no-daemon &

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   api.openai.com" >> /etc/hosts
echo "127.0.0.1   google.serper.dev" >> /etc/hosts
echo "127.0.0.1   devnet.galadriel.com" >> /etc/hosts
echo "127.0.0.1   oaidalleapiprodscus.blob.core.windows.net" >> /etc/hosts
echo "127.0.0.1   storage.googleapis.com" >> /etc/hosts
echo "127.0.0.1   oauth2.googleapis.com" >> /etc/hosts
echo "127.0.0.1   exec.bearly.ai" >> /etc/hosts
echo "127.0.0.1   api.groq.com" >> /etc/hosts
echo "127.0.0.1   galadriel.mypinata.cloud" >> /etc/hosts
echo "127.0.0.1   api.pinata.cloud" >> /etc/hosts
echo "127.0.0.1   api.anthropic.com" >> /etc/hosts

mkdir -p /run/resolvconf
echo "nameserver 127.0.0.1" > /run/resolvconf/resolv.conf

# run TLS traffic forwarder
python3.10 /app/traffic_forwarder.py 127.0.0.1 443 &

# sleep so there is time to open enclave debug logs before the server potentially crashes
# python3.10 /app/check_proxies.py

# Start the server
python3.10 /app/server.py &

sleep 20
python3.10 /app/key_manager.py
cp /app/.env /app/oracles/.env

echo "Pinging for funds"
cd /app && python3.10 oracle_ping_for_funds.py

# Starting the attestation upgrader
cd /app/oracles && python3.10 update_attestation.py &> /app/oracles/attestation_upgrader.log &

# Start oracle setup
echo "Starting the oracle!"
cd /app/oracles && python3.10 oracle.py
