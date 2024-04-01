nohup vsock-proxy 8001 api.openai.com 443 \
  --config vsock/vsock_proxy_openai.yaml &> vsock_proxy_openai.log &
nohup vsock-proxy 8002 google.serper.dev 443 \
  --config vsock/vsock_proxy_serper.yaml &> vsock_proxy_serper.log &
nohup vsock-proxy 8003 devnet.galadriel.com 443 \
  --config vsock/vsock_proxy_galadriel.yaml &> vsock_proxy_galadriel.log &
nohup vsock-proxy 8004 oaidalleapiprodscus.blob.core.windows.net 443 \
  --config vsock/vsock_proxy_windows.yaml &> vsock_proxy_windows.log &
nohup vsock-proxy 8005 storage.googleapis.com 443 \
  --config vsock/vsock_proxy_google_storage.yaml &> vsock_proxy_google_storage.log &
nohup vsock-proxy 8006 oauth2.googleapis.com 443 \
  --config vsock/vsock_proxy_google_oauth2.yaml &> vsock_proxy_google_oauth2.log &
nohup vsock-proxy 8007 exec.bearly.ai 443 \
  --config vsock/vsock_proxy_bearly.yaml &> vsock_proxy_bearly.log &
nohup vsock-proxy 8008 api.groq.com 443 \
  --config vsock/vsock_proxy_groq.yaml &> vsock_proxy_groq.log &
nohup vsock-proxy 8009 api.nft.storage 443 \
  --config vsock/vsock_proxy_nftstorage.yaml &> vsock_proxy_nftstorage.log &
nohup vsock-proxy 8010 ipfs.io 443 \
  --config vsock/vsock_proxy_ipfs.yaml &> vsock_proxy_ipfs.log &