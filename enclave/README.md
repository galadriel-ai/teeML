# Setup

```shell
sudo yum update -y
sudo yum install git -y
sudo yum install aws-nitro-enclaves-cli -y
sudo yum install aws-nitro-enclaves-cli-devel -y
sudo systemctl enable --now nitro-enclaves-allocator.service
sudo yum install docker -y
sudo systemctl enable --now docker

sudo usermod -aG ne $USER
sudo usermod -aG docker $USER
```

Verify that dependencies installed and reboot the machine:

```
nitro-cli --version
docker --version
sudo reboot
```