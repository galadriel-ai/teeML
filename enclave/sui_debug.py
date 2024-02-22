from dataclasses import dataclass
from typing import Optional

from pysui import SuiConfig
from pysui import SyncClient
from pysui.abstracts import PublicKey

sui_config = SuiConfig.default_config()
print("sui_config:", sui_config)
print("rpc_url:", sui_config.rpc_url)
print("local_config:", sui_config.local_config)
print("faucet_url:", sui_config.faucet_url)
print("socket_url:", sui_config.socket_url)
print("active_address:", sui_config.active_address)
print("environment:", sui_config.environment)
sui_client = SyncClient(sui_config)

ALIAS_NAME = "ae"

import urllib.request
# The URL you want to send a GET request to
url = "https://fullnode.devnet.sui.io"
# Use urllib to open the URL and read the response
with urllib.request.urlopen(url) as response:
    # The response object
    print("result:", response)
    # To read the content of the response
    response_text = response.read().decode('utf-8')
    print("result.text:", response_text)


@dataclass(frozen=True)
class AliasInfo:
    alias: str
    address: str
    public_key: PublicKey


def get_alias_info() -> Optional[AliasInfo]:
    for alias in sui_config.aliases:
        return AliasInfo(
            alias=alias,
            address=str(sui_config.addr4al(alias)),
            public_key=sui_config.pk4al(alias)
        )


if __name__ == '__main__':
    a = get_alias_info()
    print("AliasInfo:", a)
