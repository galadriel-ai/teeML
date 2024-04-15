import socket
import json
import subprocess
import time
from typing import Dict
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()

fetch_metrics_failures_count = 0


def _action_ps(s):
    s.send(str.encode(json.dumps({
        "action": "ps",
    })))
    response = s.recv(65536)
    return json.loads(response.decode())


def _get_enclave_metrics() -> Dict:
    try:
        cid = _get_cid()
        if not cid:
            return None
        # Create a vsock socket object
        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        s.settimeout(100.0)
        # The port should match the server running in enclave
        port = 5000
        # Connect to the server
        s.connect((cid, port))
        metrics = _action_ps(s)
        s.close()
        return metrics
    except Exception as exc:
        print("Failed to connect, exc:", exc, flush=True)
        return None

def _format_metrics(data: dict):
    global fetch_metrics_failures_count
    metrics = ""
    enclave_running = 0
    # CPU metrics
    if data:
        enclave_running = 1
        for i in range(data["cpu_count"]):
            metrics += f"# HELP cpu_usage_core{i} CPU usage percentage for core {i}\n"
            metrics += f"# TYPE cpu_usage_core{i} gauge\n"
            metrics += f"cpu_usage_core{i} {data['cpu_usage'][str(i)]}\n"
        # Memory metrics
        metrics += f"# HELP memory_used Memory used in bytes\n"
        metrics += f"# TYPE memory_used gauge\n"
        metrics += f"memory_used {data['ram_used']}\n"
        metrics += f"# HELP memory_total Total memory in bytes\n"
        metrics += f"# TYPE memory_total gauge\n"
        metrics += f"memory_total {data['ram_total']}\n"

        # Disk metrics
        metrics += f"# HELP disk_used Disk used in bytes\n"
        metrics += f"# TYPE disk_used gauge\n"
        metrics += f"disk_used {data['disk_used']}\n"
        metrics += f"# HELP disk_total Disk total in bytes\n"
        metrics += f"# TYPE disk_total gauge\n"
        metrics += f"disk_used {data['disk_total']}\n"
    else:
        fetch_metrics_failures_count += 1
    metrics += "# HELP enclave_running Whether the Enclave is up and running\n"
    metrics += "# TYPE enclave_running gauge\n"
    metrics += f"enclave_running {enclave_running}\n"
    metrics += "# HELP fetch_metrics_failures_total Total number of times the metrics fetch has failed\n"
    metrics += "# TYPE fetch_metrics_failures_total counter\n"
    metrics += f"fetch_metrics_failures_total {fetch_metrics_failures_count}\n"
    return metrics


def _get_cid():
    """
    Determine CID of Current Enclave
    """
    try:
        proc = subprocess.Popen(["/bin/nitro-cli", "describe-enclaves"],
                                stdout=subprocess.PIPE)
        output = json.loads(proc.communicate()[0].decode())
        enclave_cid = output[0]["EnclaveCID"]
        return enclave_cid
    except:
        return None


@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    data = _get_enclave_metrics()
    return _format_metrics(data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9101)
