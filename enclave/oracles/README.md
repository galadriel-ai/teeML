# Oracles

### Dependencies

Install Bacalhau client

```shell
curl -sL https://get.bacalhau.org/install.sh | bash
```

### Deployment

```shell
cd oracles
conda activate agent-network
pkill -f oracle_iterator.py
nohup python oracle_iterator.py &> logs.log &
```