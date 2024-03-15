# Attestation Verification

System requirements:
* aws EC2 instance with Nitro Enclave support (tested on m5.xlarge EC2 instance)
  * must check Nitro Enclave enabled in the instance creation
* Amazon Linux (tested on Amazon Linux 2023 AMI 2023.3.20240312.0 x86_64 HVM kernel-6.1)
* x86_64 architecture CPU

### 0. Prerequisites

* Easiest is to use EC2 image with docker and nitro-cli installed
* If prefer an additional linux distro support need to do additional steps 
* If Nitro Enclave kernel driver is not included on chosen linux kernel, it needs to be installed manually. See more here: https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md

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

### 2. Setup python

```shell
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade pyOpenSSL
```

### 3. Verify attestation

Attestation file is saved in attestation_doc_b64.txt. You can also download this
from the blockchain from the Oracle contract or execute the `python3 get_attestation.py`.

Optionally, you can download the root.pem from Amazon: https://aws-nitro-enclaves.amazonaws.com/AWS_NitroEnclaves_Root-G1.zip

```shell
# The argument is the PCR0 from the enclave image build step.
python3 verify.py b3a233e8a1d2682455777643d5a793c9d231754ebd89e8ffc14b07a21da0de07920763e87f8cc6eb3a6d362beeb4f541
```
