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

# execute on the enclave Host VM - sign any message
python client.py --cid <enclave cid> --action sign_message --message "hello"
# execute anywhere if you have the public key of the enclave
python verify_signature.py --message "hello" --signature <signature>
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
  --args "0xabcdef00" 0xd3eae32a81e92ba335ef48bbcff83f15c312f6bb0dffca139775d53c2103d12a "0x27cf3f13902cdab041b7d16ca0f2eefd7f04a8fc6cb4e971fe753b6e494ea7cb05a4bedda8341dd5550c197c41af1d39b90075972fb39c15a8707aef1f09f2bf"
```
