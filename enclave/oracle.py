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
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_txn import SyncTransaction

sui_config = SuiConfig.default_config()
sui_client = SyncClient(sui_config)

MIN_BALANCE = 1000000000

ORACLE_PACKAGE_ID = "0xcd25681ebc6975732c2910705a900550e2164cdbcad5d5bd05c7558c79b4ed69"
TARGET = f"{ORACLE_PACKAGE_ID}::oracle::set_attestation"
PUBLIC_KEY_STORAGE_OBJECT_ID = "0xcf57d87c271940a259093f28007beb7c0bc6178122f56b24cda68d6480d6fbdb"


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


def _send_tx(enclave_address: str, attestation_doc_b64: str):
    print("=== SEND TX ===")
    try:
        arguments = [
            ObjectID(PUBLIC_KEY_STORAGE_OBJECT_ID),
            SuiAddress(enclave_address),
            attestation_doc_b64
        ]
        for_owner: SuiAddress = sui_client.config.active_address
        print("  for_owner:", for_owner)
        txn = SyncTransaction(client=sui_client, initial_sender=for_owner)
        txn.move_call(target=TARGET, arguments=arguments, type_arguments=[])
        rpc_result: SuiRpcResult = txn.execute(gas_budget=100000000,
                                               use_gas_object=None)
        if rpc_result.is_ok():
            print("OK")
        else:
            print("NOT OK, result", rpc_result.result_string)
        print("rpc_result:", rpc_result)
        status = rpc_result.result_data.effects.status
        print("status:", status)
        if not status.succeeded:
            print("Failed")
        else:
            print("Succeed")

        print("Effects:", rpc_result.result_data.effects)
    except Exception as exc:
        print("Send TX exception:", exc)
    print("=== SEND TX DONE ===")


def main():
    alias = _get_alias_info()
    print("Alias:", alias)
    _wait_for_funds(alias)
    _send_tx(alias.address, "IamAnEnclave")
    time.sleep(60)


if __name__ == '__main__':
    main()
