import time
from dataclasses import dataclass
from typing import Optional

from pysui import SuiAddress

from pysui import SuiConfig
from pysui import SuiRpcResult
from pysui import SyncClient
from pysui.abstracts import PublicKey

from pysui.sui.sui_builders.get_builders import GetCoinTypeBalance
from pysui.sui.sui_txresults import SuiCoinBalance

sui_config = SuiConfig.default_config()
sui_client = SyncClient(sui_config)

MIN_BALANCE = 1000000000


@dataclass(frozen=True)
class AliasInfo:
    alias: str
    address: str
    public_key: PublicKey


def _get_alias_info() -> Optional[AliasInfo]:
    for alias in sui_config.aliases:
        return AliasInfo(
            alias=alias,
            address=str(sui_config.addr4al(alias)),
            public_key=sui_config.pk4al(alias)
        )


def _generate_data_block(data_block: dict, method: str, params: list) -> dict:
    """Build the json data block for Rpc."""
    data_block["method"] = method
    data_block["params"] = params
    return data_block


def _get_balance(address: SuiAddress):
    builder = GetCoinTypeBalance(owner=address)
    result: SuiRpcResult = sui_client.execute(builder=builder)
    if result.is_ok():
        coin_balance: SuiCoinBalance = result.result_data
        total_balance = coin_balance.total_balance
        return total_balance
    else:
        print("Not OK")


def _wait_for_funds(alias: AliasInfo):
    while True:
        balance = _get_balance(SuiAddress(alias.address))
        print("balance:", balance)
        if int(balance) > MIN_BALANCE:
            print("Got funds!\n")
            return
        time.sleep(3)


def main():
    alias = _get_alias_info()
    print("Alias:", alias)
    _wait_for_funds(alias)


if __name__ == '__main__':
    main()
