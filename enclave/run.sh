#!/bin/bash

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   api.openai.com" >> /etc/hosts
echo "127.0.0.1   google.serper.dev" >> /etc/hosts
echo "127.0.0.1   testnet.galadriel.com" >> /etc/hosts

python3.10 /app/traffic_forwarder.py 127.0.0.1 443 &

# Decrypt the .env file
aws kms decrypt \
    --ciphertext-blob fileb://.env.encrypted \
    --key-id arn:aws:kms:eu-central-1:928498401497:key/b539ad32-e557-4479-aaa0-73344c3b9cf6 \
    --output text \
    --query Plaintext | base64 \
    --decode > .env

# Decrypt the service account key
aws kms decrypt \
    --ciphertext-blob fileb://sidekik-ai.json.encrypted \
    --key-id arn:aws:kms:eu-central-1:928498401497:key/b539ad32-e557-4479-aaa0-73344c3b9cf6 \
    --output text \
    --query Plaintext | base64 \
    --decode > sidekik-ai-5d0110872b7a.json

#/app/kmstool_enclave_cli decrypt \
#  --region "region" \
#  --aws-access-key-id "access" \
#  --aws-secret-access-key "secret" \
#  --aws-session-token "token" \
#  --ciphertext "ciphertext"

python3.10 /app/key_manager.py

# sleep so there is time to open enclave debug logs before the server potentially crashes
sleep 30
python3.10 /app/check_proxies.py

# Start the server
python3.10 /app/server.py

# Start oracle setup
# python3.10 /app/oracle.py
