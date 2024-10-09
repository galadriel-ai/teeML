### ⚠️ NB! This project is deprecated as of 09.10.24 ⚠️

# teeML

teeML: Trusted Execution Environment for Machine Learning Inference.

The purpose of this repository to enable the querying of model APIs and external tools in a low latency, low cost, and verifiable manner. To do so, it contains everything needed to execute the [Galadriel oracle](https://github.com/galadriel-ai/contracts) in an [AWS Nitro enclave](https://aws.amazon.com/ec2/nitro/nitro-enclaves/), and verify its execution.

A high level overview is given in [docs.galadriel.com](https://docs.galadriel.com/how-it-works#tee).

### This project

The oracle currently supports calling the following, all of which is also supported by the TEE setup:

* LLMs from OpenAI and Groq
* Image generation with OpenAI's DALL-E
* Code execution via E2B's code interpreter API
* Web search via Serper API

See details of supported tools in the [oracle reference](https://docs.galadriel.com/reference/overview).

This project is divided into 3 parts in corresponding directories:

1. `enclave` - this where the enclave is built and run
2. `admin` - this is where the admin can interact with the encalve and verify 
attestation doc
3. `verify` - minimal version of the admin to only validate the enclave's 
attestation doc

If you came here to just learn how to verify the enclave's attestation doc then 
see this [README](./verify/README.md)

### Prerequisites

1. Setup an AWS Nitro Enclave-supported VM.
1. Strongly recommended: go through the following tutorials before proceeding.
    1. [Nitro Enclave environment setup](https://catalog.workshops.aws/nitro-enclaves/en-US/0-getting-started/prerequisites)
    1. [Nitro Enclaves CLI](https://catalog.workshops.aws/nitro-enclaves/en-US/1-my-first-enclave/1-1-nitro-enclaves-cli)
    1. [Verifying the root of trust](https://docs.aws.amazon.com/enclaves/latest/user/verify-root.html)

### Create and run an AWS Nitro Enclave

* The enclave comes with `libnsm.so` included and Python calls it over C bindings.
* `libnsm` is a Rust shared object with a Python wrapper around it.

Setup the admin `.env` file that is going to be sent to the enclave once it starts:

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
