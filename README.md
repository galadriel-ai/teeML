# AWS Enclave

Prerequirements:
* setup aws nitro enclave supported VM
* do bunch of more stuff...
  * https://catalog.workshops.aws/nitro-enclaves/en-US/0-getting-started/prerequisites
  * https://catalog.workshops.aws/nitro-enclaves/en-US/1-my-first-enclave/1-1-nitro-enclaves-cli
  * https://www.notion.so/nftport/TEE-b4069289b4bd49ae810010eceaece2d6
  * https://docs.aws.amazon.com/enclaves/latest/user/verify-root.html

### Create and run an AWS Nitro Enclave

* enclave comes with `lbnsm.so` and python is calling it over C binding
* the libnsm is rust shared object with python wrapper around it

```shell
sudo systemctl stop nitro-enclaves-allocator.service
vi /etc/nitro_enclaves/allocator.yaml
sudo systemctl start nitro-enclaves-allocator.service && sudo systemctl enable nitro-enclaves-allocator.service

# Setup vsock proxy to connect to SUI fullnode
cd enclave
vsock-proxy 8001 fullnode.devnet.sui.io 443 --config vsock/vsock_proxy_sui_devnet.yaml
vsock-proxy 8002 api.openai.com 443 --config vsock/vsock_proxy_openai.yaml
sudo vi /etc/nitro_enclaves/vsock-proxy.yaml
sudo systemctl start nitro-enclaves-vsock-proxy.service
```

```shell
# Optional: stop the enclave
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
[ "$ENCLAVE_ID" != "null" ] && nitro-cli terminate-enclave --enclave-id ${ENCLAVE_ID}
nitro-cli describe-enclaves # Optional: see if any enclaves are running

cd enclave
docker build ./ -t "galadriel"
nitro-cli build-enclave --docker-uri "galadriel:latest" --output-file "galadriel.eif"
nitro-cli run-enclave --cpu-count 2 --memory 15000 --eif-path galadriel.eif
nitro-cli describe-enclaves # Optional: see the enclave information and CID
nitro-cli console --enclave-id <enclave cid> # Optional: if running in debug mode
```

Enclave data example:
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
python3 client.py --cid <enclave cid> --action get_attestation_doc

# execute anywhere if you have the attestation doc b64
# this script verifies the enclave's attestation doc to AWS root certificate
# also prints out the public key of the enclave and saves to file
python verify.py <pcr0 of the enclave> 

# once attestation verified and public key saved
python sui_publish_attestation.py
```

### Deterministic enclave image building

1. Need deterministic docker build? How?
2. Given the same docker image is the enclave always the same?


### Crypto references

Python examples on how to create keys, create signature and validate.

RSA:
```shell
python script_sign_message_rsa.py
```

secp256k1:
```shell
python script_sign_message_secp256k1.py
```

Running on SUI Move:

Download some version of sui-mainnet binary from github releases, for example v1.17.3.

Run the localnet:
```shell
./sui-mainnet-v1.17.3-macos-arm64/target/release/sui-test-validator-macos-arm64
```

Another window:
```shell
# get funds to deploy and send tx
sui client active-address
curl --location --request POST 'http://127.0.0.1:9123/gas' \
--header 'Content-Type: application/json' \
--data-raw '{
    "FixedAmountRequest": {
        "recipient": "0x5a1c3cc19acfd04538fd7ae83195eb394d1836e4e3c085ce7b5cae9a74908dbc"
    }
}'

# deploy contract and call
cd sui/secpk256k1
sui move build
sui client publish --gas-budget 100000000

sui client call \
  --package 0x23a64559e81f02cdda12216d5849f648b23ae89c24b8e37f9fe5bd303fee9e3e \
  --module secpk256k1 \
  --function validateSignature \
  --gas-budget 100000000 \
  --args "0xabcdef00" 0x9eb035a86cdbe0a0a04b9c39bcf71e835af1a4f0c6bb26b611f31bccc02d8feb "0x27cf3f13902cdab041b7d16ca0f2eefd7f04a8fc6cb4e971fe753b6e494ea7cb05a4bedda8341dd5550c197c41af1d39b90075972fb39c15a8707aef1f09f2bf"
  
  
Package ID: 0x192a913ca8e84ff9a6bd2f3b038a5460240c73aa037859630606147ddec14f20
KeyStorage ID: 0x9eb035a86cdbe0a0a04b9c39bcf71e835af1a4f0c6bb26b611f31bccc02d8feb
```


# Attestation

0. we deploy oracle contract

1. Open source oracle codebase
2. When oracle starts, 
   * it will generate a keypair and store the private key in the enclave
   * we ask the public key and fund the account and give write access to oracle contract
   * oracle polls until it has funds
   * once funds arrive, it will generate attestation and push attestation and public key to the chain in the oracle

3. Agent dev
   * off chain read the oracle public key from the chain 
   * create AgentRun with that public key

# Admin

* get public address of the enclave
* send SUI:
```shell
sui client transfer-sui \
  --to 0x67ddc499ac49ea7fe6310bb3937083a323da8cd1f172664a68dab597671068af \
  --gas-budget 50000000000 \
  --amount 50000000000 \
  --sui-coin-object-id 0x597e3ad88ee80c1ad0285f03076ff648af074e6661257bd21f9f35fae4a8eaa5
```