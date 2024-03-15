# teeML

teeML is a Trusted Execution Environment (TEE) based AI inference.

Currently supports calling:
* openai gpt models
* generating images with DALL-E

This project is divided into 3 parts:
1. enclave - this where the enclave is built and run
2. admin - this is where the admin can interact with the encalve and verify 
attestation doc
3. verify - minimal version of the admin to only validate the enclave's 
attestation doc

If you came here to just learn how to verify the enclave's attestation doc then 
see this [README](./verify/README.md)

### Prerequirements

* setup aws nitro enclave supported VM
* recommended to go through tutorials first before running...
    * https://catalog.workshops.aws/nitro-enclaves/en-US/0-getting-started/prerequisites
    * https://catalog.workshops.aws/nitro-enclaves/en-US/1-my-first-enclave/1-1-nitro-enclaves-cli
    * https://www.notion.so/nftport/TEE-b4069289b4bd49ae810010eceaece2d6
    * https://docs.aws.amazon.com/enclaves/latest/user/verify-root.html

### Create and run an AWS Nitro Enclave

* enclave comes with `lbnsm.so` and python is calling it over C binding
* the libnsm is rust shared object with python wrapper around it

Setup the admin .env file that is going to be sent to the enclave once it starts:
```shell
cd admin
cp .env.template .env # update the .env file with the correct values
```

Run the enclave:
```shell

cd enclave
./run_proxies.sh
./run_enclave.sh
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
