# AWS Enclave

### Create and run an AWS Nitro Enclave

* enclave comes with `lbnsm.so` and python is calling it over C binding
* the libnsm is rust shared object with python wrapper around it

```shell
# Optional: stop the enclave
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
[ "$ENCLAVE_ID" != "null" ] && nitro-cli terminate-enclave --enclave-id ${ENCLAVE_ID}
nitro-cli describe-enclaves # Optional: see if any enclaves are running

cd enclave
docker build ./ -t "galadriel"
nitro-cli build-enclave --docker-uri "galadriel:latest" --output-file "galadriel.eif"
nitro-cli run-enclave --cpu-count 2 --memory 2048 --eif-path galadriel.eif
nitro-cli describe-enclaves # Optional: see the enclave information and CID
```

Enclave data
```json
{
  "Measurements": {
    "HashAlgorithm": "Sha384 { ... }",
    "PCR0": "e11704780b078425d45dac5f72b523264406531ff6f4611aba908c320a20b5f2ec81404d21f6f0aef415adf2590d4129",
    "PCR1": "52b919754e1643f4027eeee8ec39cc4a2cb931723de0c93ce5cc8d407467dc4302e86490c01c0d755acfe10dbf657546",
    "PCR2": "b67f9d7d0a69f6eaf2cba87ffbe983eb4491dbb4ac4aef07528cd75327bfd8b5d5122c4f73c61c3836e57363306141cc"
  }
}
```

### Run the client

```shell
cd client
pip install -r requirements.txt
pip install --upgrade pyOpenSSL

# execute on the enclave Host VM
python client.py <enclave_cid>

# execute anywhere if you have the attestation doc b64
python verify.py <pcr0 of the enclave> 
```




### Deterministic enclave image building

1. Need deterministic docker build? How?
2. Given the same docker image is the enclave always the same?