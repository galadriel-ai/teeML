nohup vsock-proxy 8001 api.openai.com 443 --config vsock/vsock_proxy_openai.yaml &> vsock_proxy_openai.log &
nohup vsock-proxy 8002 fullnode.devnet.sui.io 443 --config vsock/vsock_proxy_sui_devnet.yaml &> vsock_proxy_sui.log &
nohup vsock-proxy 8003 ipfs.io 443 --config vsock/vsock_proxy_ipfs.yaml &> vsock_proxy_ipfs.log &
nohup vsock-proxy 8004 bootstrap.production.bacalhau.org 1234 --config vsock/vsock_proxy_bacalhau.yaml &> vsock_proxy_bacalhau.log &
nohup vsock-proxy 8005 google.serper.dev 443 --config vsock/vsock_proxy_serper.yaml &> vsock_proxy_serper.log &