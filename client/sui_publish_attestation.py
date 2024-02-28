from pysui import SuiAddress
from pysui import SuiConfig
from pysui import SuiRpcResult
from pysui import SyncClient
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_txn import SyncTransaction

PUBLIC_KEY_PATH = "enclave_public_key.txt"
ATTESTATION_PATH = "attestation_doc_b64.txt"

NATIVE_COIN = "0x2::sui::SUI"

ORACLE_PACKAGE_ID = "0xe426679d385dd3c3a43a146bd7e770e00a4513d0ad99c28f9df9d3e3e3b92288"
TARGET = f"{ORACLE_PACKAGE_ID}::oracle::set_attestation"
PUBLIC_KEY_STORAGE_OBJECT_ID = "0x603d4c142e9318e6492194f84c250997c1afca0752cbb87be41e2b4bf63ce0e3"

sui_config = SuiConfig.default_config()
sui_client = SyncClient(sui_config)


def execute(enclave_address: str, attestation_doc_b64: str):
    print("publishing attestation")
    arguments = [
        ObjectID(PUBLIC_KEY_STORAGE_OBJECT_ID),
        SuiAddress(enclave_address),
        attestation_doc_b64
    ]
    for_owner: SuiAddress = sui_client.config.active_address
    print("  for_owner:", for_owner)
    txn = SyncTransaction(client=sui_client, initial_sender=for_owner)
    txn.move_call(target=TARGET, arguments=arguments, type_arguments=[])
    rpc_result: SuiRpcResult = txn.execute(gas_budget=100000000, use_gas_object=None)
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


def _read_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    public_key = _read_file(PUBLIC_KEY_PATH)
    print("Got public key from file:", public_key)
    attestation_doc_b64 = _read_file(ATTESTATION_PATH)
    execute(public_key, attestation_doc_b64)


if __name__ == '__main__':
    main()
