# Enclave client

## Admin

Admin is responsible for:
1. Creating the enclave image
2. Starting the enclave
3. Getting the enclave public key and attestation doc
4. Publishing the enclave public key and attestation doc to the Oracle Contract

Flow:

```shell
# Request attestation doc from the enclave
python client.py --cid <enclave cid> --action get_attestation_doc
# Verify the attestation doc
python verify.py <pcr0 of the enclave> 
# Publish the enclave public key and attestation doc to the Oracle Contract
python sui_publish_attestation.py
```

## Extra

Devnet faucet:

```shell
curl --location --request POST 'https://faucet.devnet.sui.io/gas' \
--header 'Content-Type: application/json' \
--data-raw '{
    "FixedAmountRequest": {
        "recipient": "0xdce322a48d4649fa14490962c5fc5daeaa0bb48d9249c007fc8316092250feb3"
    }
}'
```
