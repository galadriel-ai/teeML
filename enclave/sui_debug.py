from dataclasses import dataclass
from typing import Optional

from pysui import SuiConfig
from pysui import SyncClient
from pysui.abstracts import PublicKey

sui_config = SuiConfig.default_config()
sui_client = SyncClient(sui_config)

ALIAS_NAME = "ae"


@dataclass(frozen=True)
class AliasInfo:
    alias: str
    address: str
    public_key: PublicKey


def get_alias_info() -> Optional[AliasInfo]:
    for alias in sui_config.aliases:
        return AliasInfo(
            alias=alias,
            address=sui_config.addr4al(alias),
            public_key=sui_config.pk4al(alias)
        )


if __name__ == '__main__':
    a = get_alias_info()
    print("AliasInfo:", a)
