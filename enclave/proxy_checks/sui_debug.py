"""from dataclasses import dataclass
from typing import Optional

from pysui import SuiConfig
from pysui import SyncClient
from pysui.abstracts import PublicKey"""


def _generate_data_block(data_block: dict, method: str, params: list) -> dict:
    """Build the json data block for Rpc."""
    data_block["method"] = method
    data_block["params"] = params
    return data_block


def execute() -> (bool, str):
    try:
        print("\n=== Making SUI call ===")
        import httpx
        from pysui.sui.sui_builders.get_builders import (
            GetRpcAPI,
        )

        builder_rpc_api = GetRpcAPI()
        with httpx.Client(http2=False, verify=False) as client:
            rpc_api_result = client.post(
                "https://fullnode.devnet.sui.io",
                headers=builder_rpc_api.header,
                json=_generate_data_block(
                    builder_rpc_api.data_dict,
                    builder_rpc_api.method,
                    builder_rpc_api.params,
                ),
            )
            print("\nrpc_api_result:", rpc_api_result)
            if not rpc_api_result.status_code == 200:
                return False, f"Status code from API: {rpc_api_result.status_code}"
            print("rpc_api_result.content", rpc_api_result.json()["result"]["info"])
        print("=== SUI Call done ===\n")
        return True, ""
    except Exception as exc:
        return False, str(exc)
