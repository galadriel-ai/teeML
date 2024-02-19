from typing import List

from pysui import SuiAddress
from pysui import SuiConfig
from pysui import SuiRpcResult
from pysui import SyncClient
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_types import SuiU8

PACKAGE_ID = "0x86507e70c0fe9a0a000e657e947515cca8a54359bc64f25047ad35c2d213fb9b"

# TODO: replace config path!
suiConfig = SuiConfig.pysui_config("/Users/kaspar/.sui/sui_config")
sui_client = SyncClient(suiConfig)

for_owner: SuiAddress = sui_client.config.active_address
target = f"{PACKAGE_ID}::secpk256k1::validateSignature"


def convert_to_u8_vector(hex_string: str) -> List[SuiU8]:
    result = []
    for i in list(bytearray.fromhex(hex_string)):
        result.append(SuiU8(i))
    return result


def get_arguments():
    arguments = [
        convert_to_u8_vector("abcdef00"),
        convert_to_u8_vector("027f5fc5283d80756a59b00ab26d2ea914f5d3d35deae839af8806e8f042dd0668"),
        convert_to_u8_vector("27cf3f13902cdab041b7d16ca0f2eefd7f04a8fc6cb4e971fe753b6e494ea7cb05a4bedda8341dd5550c197c41af1d39b90075972fb39c15a8707aef1f09f2bf"),
    ]
    return arguments


def send_tx():
    arguments = get_arguments()
    txn = SyncTransaction(client=sui_client, initial_sender=for_owner)
    txn.move_call(target=target, arguments=arguments, type_arguments=[])
    rpc_result: SuiRpcResult = txn.execute(gas_budget=100000000, use_gas_object=None)
    status = rpc_result.result_data.effects.status
    print("status:", status)
    if not status.succeeded:
        print("Failed")
    else:
        print("Succeed")

    print("Effects:", rpc_result.result_data.effects)


if __name__ == '__main__':
    send_tx()
