nohup vsock-proxy 8000 secretsmanager.eu-central-1.amazonaws.com 443 \
  --config vsock/vsock_proxy_kms.yaml &> vsock_proxy_kms.log &
nohup vsock-proxy 8001 api.openai.com 443 \
  --config vsock/vsock_proxy_openai.yaml &> vsock_proxy_openai.log &
nohup vsock-proxy 8002 google.serper.dev 443 \
  --config vsock/vsock_proxy_serper.yaml &> vsock_proxy_serper.log &
nohup vsock-proxy 8003 testnet.galadriel.com 443 \
  --config vsock/vsock_proxy_galadriel.yaml &> vsock_proxy_galadriel.log &