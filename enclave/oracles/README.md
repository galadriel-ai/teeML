# Oracles

### Deployment

```shell
cd oracles
conda activate agent-network
pkill -f oracle_iterator.py
nohup python oracle_iterator.py &> logs.log &
```