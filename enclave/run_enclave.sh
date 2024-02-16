ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
[ "$ENCLAVE_ID" != "null" ] && nitro-cli terminate-enclave --enclave-id ${ENCLAVE_ID}

docker build ./ -t "galadriel"
nitro-cli build-enclave --docker-uri "galadriel:latest" --output-file "galadriel.eif"
nitro-cli run-enclave --cpu-count 2 --memory 2048 --eif-path galadriel.eif
nitro-cli describe-enclaves