nohup vsock-proxy 8001 api.openai.com 443 \
  --config vsock/vsock_proxy_openai.yaml -w 20 &> vsock_proxy_openai.log &
nohup vsock-proxy 8002 google.serper.dev 443 \
  --config vsock/vsock_proxy_serper.yaml -w 20 &> vsock_proxy_serper.log &
nohup vsock-proxy 8003 devnet.galadriel.com 443 \
  --config vsock/vsock_proxy_galadriel.yaml -w 20 &> vsock_proxy_galadriel.log &
nohup vsock-proxy 8004 oaidalleapiprodscus.blob.core.windows.net 443 \
  --config vsock/vsock_proxy_windows.yaml -w 20 &> vsock_proxy_windows.log &
nohup vsock-proxy 8005 storage.googleapis.com 443 \
  --config vsock/vsock_proxy_google_storage.yaml -w 20 &> vsock_proxy_google_storage.log &
nohup vsock-proxy 8006 oauth2.googleapis.com 443 \
  --config vsock/vsock_proxy_google_oauth2.yaml -w 20 &> vsock_proxy_google_oauth2.log &
nohup vsock-proxy 8007 api.e2b.dev 443 \
  --config vsock/vsock_proxy_e2b.yaml -w 20 &> vsock_proxy_e2b.log &
nohup vsock-proxy 8008 api.groq.com 443 \
  --config vsock/vsock_proxy_groq.yaml -w 20 &> vsock_proxy_groq.log &
nohup vsock-proxy 8009 galadriel.mypinata.cloud 443 \
  --config vsock/vsock_proxy_ipfs.yaml -w 20 &> vsock_proxy_ipfs.log &
nohup vsock-proxy 8010 api.pinata.cloud 443 \
  --config vsock/vsock_proxy_pinata.yaml -w 20 &> vsock_proxy_pinata.log &
