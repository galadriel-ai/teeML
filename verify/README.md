# Attestation Verification

This directory contains instructions and code for verifying the oracle running inside the TEE.

### 0. Prerequisites

System requirements:

* An AWS EC2 instance with Nitro Enclave support (we have tested on `m5.xlarge` EC2 instance).
    * You must enable the "Nitro Enclave enabled" option when creating the instance
    * Amazon Linux (tested on `Amazon Linux 2023 AMI 2023.3.20240312.0 x86_64 HVM kernel-6.1`)
    * x86_64 architecture CPU
    * It is easiest to use an EC2 image with Docker and `nitro-cli` installed
    * If you want to support a different linux distro, you need additional configuration
    * If the Nitro Enclave kernel driver is not included on chosen linux kernel, it needs to be installed manually. See more [here](https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md)


For Amazon Linux:

```shell
sudo yum update -y
sudo dnf install aws-nitro-enclaves-cli -y
sudo dnf install aws-nitro-enclaves-cli-devel -y
sudo systemctl enable --now nitro-enclaves-allocator.service
sudo usermod -aG ne $USER

sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker $(whoami)

sudo yum install python-pip -y

sudo reboot
```

### 1. Create the enclave image

```shell
nitro-cli build-enclave --docker-uri "ghcr.io/galadriel-ai/aws_enclave:v0.0.2" --output-file "galadriel.eif"
```

You need to get exactly the same hashes:

```shell
Enclave Image successfully created.
{
  "Measurements": {
    "HashAlgorithm": "Sha384 { ... }",
    "PCR0": "b3a233e8a1d2682455777643d5a793c9d231754ebd89e8ffc14b07a21da0de07920763e87f8cc6eb3a6d362beeb4f541",
    "PCR1": "52b919754e1643f4027eeee8ec39cc4a2cb931723de0c93ce5cc8d407467dc4302e86490c01c0d755acfe10dbf657546",
    "PCR2": "3bf7565751ec5865be41221c62fc7e69429a0d9a219a91ba858fd4b2fa31fac6cc416d5eca29cc9405a83749c896e494"
  }
}
```

### 2. Setup Python

```shell
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade pyOpenSSL
```

### 3. Verify attestation

Optionally, you can download the attestation directly from blockchain with
`python3 get_attestation.py` and verify it is the same as
`attestation_doc_b64.txt` in this repo.

Optionally, you can download the root.pem from Amazon and verify it is the same 
as the `root.pem` in this repo: https://aws-nitro-enclaves.amazonaws.com/AWS_NitroEnclaves_Root-G1.zip

```shell
# The argument is the PCR0 from the enclave image build step.
python3 verify.py b3a233e8a1d2682455777643d5a793c9d231754ebd89e8ffc14b07a21da0de07920763e87f8cc6eb3a6d362beeb4f541
```
