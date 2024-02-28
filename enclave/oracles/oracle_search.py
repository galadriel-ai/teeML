import json
import time
from dataclasses import dataclass
from typing import List

from pysui import SuiAddress
from pysui import SuiConfig
from pysui import SuiRpcResult
from pysui import SyncClient
from pysui.sui.sui_builders.get_builders import GetDynamicFields
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_types.scalars import SuiU64

import settings
from vector_search import vector_search_use_case

suiConfig = SuiConfig.pysui_config(settings.SUI_CONFIG_PATH)

sui_client = SyncClient(suiConfig)


@dataclass
class VectorQueryAndResponse:
    cid: str
    embeddings: List[int]
    response: str = None
    status: str = None  # SUCCEEDED || FAILED


calls_made = 0
queries_and_responses = {}


def _send_add_response_tx(k: SuiU64, response: str) -> bool:
    """
    Sends tx to add response on Oracle
    :param k:
    :param response:
    :return: boolean representing success or failure
    """
    for_owner: SuiAddress = sui_client.config.active_address
    target = f"{settings.ORACLE_PACKAGE_ID}::oracle::addVectorSearchResponse"
    arguments = [ObjectID(settings.VECTOR_SEARCH_RESPONSES_OBJECT_ID), k, response]
    txn = SyncTransaction(client=sui_client, initial_sender=for_owner)
    txn.move_call(target=target, arguments=arguments, type_arguments=[])
    rpc_result: SuiRpcResult = txn.execute(gas_budget=100000000, use_gas_object=None)
    status = rpc_result.result_data.effects.status
    print("status:", status)
    if not status.succeeded:
        print("Failed")
        return False
    return True


def _index_prompts():
    global calls_made
    response = sui_client.get_object(
        ObjectID(settings.VECTOR_SEARCH_OBJECT_ID)
    )
    calls_made += 1
    content = response.result_data.content
    queries_id = content.fields["queries"]["fields"]["id"]["id"]
    response = sui_client.execute(
        GetDynamicFields(ObjectID(queries_id))
    )
    calls_made += 1
    for row in response.result_data.data:
        entry = json.loads(row.name.replace("'", '"'))
        k = entry["value"]
        if k not in queries_and_responses:
            response = sui_client.get_object(ObjectID(row.object_id))
            calls_made += 1
            value = response.result_data.content.fields["value"]["fields"]
            queries_and_responses[k] = VectorQueryAndResponse(
                cid=value["cid"],
                embeddings=value["embeddings"],
            )


def _index_responses():
    global calls_made
    response = sui_client.get_object(
        ObjectID(settings.VECTOR_SEARCH_RESPONSES_OBJECT_ID)
    )
    calls_made += 1
    content = response.result_data.content
    response_id = content.fields["responses"]["fields"]["id"]["id"]
    response = sui_client.execute(
        GetDynamicFields(ObjectID(response_id))
    )
    calls_made += 1
    for row in response.result_data.data:
        entry = json.loads(row.name.replace("'", '"'))
        k = entry["value"]
        print("k:", k)
        if k in queries_and_responses and not queries_and_responses[k].response:
            response = sui_client.get_object(ObjectID(row.object_id))
            calls_made += 1
            value = response.result_data.content.fields["value"]
            queries_and_responses[k].response = value


def _debug_print_queries():
    print("Queries indexed")
    print("Calls Made:", calls_made)
    unanswered = 0
    for key, value in queries_and_responses.items():
        print(f"    key: {key}, "
              f"cid: {value.cid}, "
              f"embeddings length: {len(value.embeddings)}, "
              f"response: {_shorten_string(value.response)}, "
              f"status: {value.status}")
        if not value.response:
            unanswered += 1
    print("Unanswered queries:", unanswered, flush=True)


def _shorten_string(string: str) -> str:
    if string:
        if len(string) > 20:
            return string[:20] + "..."
        return string


def _answer_unanswered_prompts():
    for k, query_and_response in queries_and_responses.items():
        if not query_and_response.response:
            response = vector_search_use_case.execute(query_and_response.cid, query_and_response.embeddings)
            if response:
                if _send_add_response_tx(SuiU64(k), response):
                    queries_and_responses[k].response = response


def _listen():
    while True:
        try:
            _index_prompts()
            _index_responses()
        except Exception as exc:
            print("Failed to index chain, exc:", exc)
        _debug_print_queries()
        _answer_unanswered_prompts()
        time.sleep(10)


def main():
    _listen()
    # _get_openai_answer("hello world")


if __name__ == '__main__':
    main()
