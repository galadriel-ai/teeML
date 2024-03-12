# Attestation Verification

System requirements:
* aws EC2 instance with Nitro Enclave support (tested on m5.xlarge EC2 instance)
  * must check Nitro Enclave enabled in the instance creation
* Amazon Linux (tested on 2023 AMI 2023.3.20240219.0 x86_64 HVM kernel-6.1)
* x86_64 architecture CPU

### 0. Prerequisites

* Easiest is to use EC2 image with docker and nitro-cli installed
* If prefer an additional linux distro support need to do additional steps 
* If Nitro Enclave kernel driver is not included on chosen linux kernel, it needs to be installed manually. See more here: https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md

```shell
sudo apt-get update
# Docker install dependencies
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Actual install
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo usermod -aG docker $USER
# logout and login

# Nitro-cli install
sudo apt-get update
sudo apt-get install build-essential linux-modules-extra-aws gcc-12 -y
sudo insmod /usr/lib/modules/$(uname -r)/kernel/drivers/virt/nitro_enclaves/nitro_enclaves.ko

sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

git clone https://github.com/aws/aws-nitro-enclaves-cli.git
cd aws-nitro-enclaves-cli/

THIS_USER="$(whoami)"
export NITRO_CLI_INSTALL_DIR=/
make nitro-cli
make vsock-proxy
sudo make NITRO_CLI_INSTALL_DIR=/ install
source /etc/profile.d/nitro-cli-env.sh
echo source /etc/profile.d/nitro-cli-env.sh >> ~/.bashrc
nitro-cli-config -i
```


### On Amazon Linux 2023

```shell
sudo yum update -y
sudo dnf install aws-nitro-enclaves-cli -y
sudo dnf install aws-nitro-enclaves-cli-devel -y
sudo yum install git -y
sudo usermod -aG ne $USER
sudo usermod -aG docker $USER

# log out and log back in
sudo systemctl enable --now nitro-enclaves-allocator.service
sudo systemctl enable --now docker
```

### 1. Create the Docker image

```shell
git clone git@github.com:galadriel-ai/aws-enclave.git
cd aws-enclave/verify
# TODO:
cp .env.template .env
nitro-cli build-enclave --docker-uri "ghcr.io/galadriel-ai/aws_enclave:latest" --output-file "galadriel.eif"
```

### 2. Create enclave image

```shell
nitro-cli build-enclave --docker-uri "galadriel:latest" --output-file "galadriel.eif"
```

### 3. Verify attestation

```shell
python3 verify.py <pcr0 of the enclave> # get the pcr0 from the previous step
```