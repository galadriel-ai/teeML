import asyncio
import json
import time
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

from pysui import AsyncClient
from pysui import SuiAddress
from pysui import SuiConfig
from pysui.sui.sui_builders.get_builders import GetDynamicFields
from pysui.sui.sui_txn import AsyncTransaction
from pysui.sui.sui_types.scalars import ObjectID
from pysui.sui.sui_types.scalars import SuiU64

import settings
from functions import call_function_use_case
from repository.openai_repository import OpenAiRepository
from vector_search import vector_search_use_case
from repository.openai_repository import OpenAiResult


@dataclass
class LlmData:
    id: str
    index: int
    content: str
    type: str
    function_run_id: str


@dataclass
class AgentRun:
    id: str
    owner: str
    knowledge_base: str
    knowledge_base_description: str
    max_iterations: int
    is_finished: bool
    llm_data_id: str
    llm_data: List[LlmData]


@dataclass
class RegisteredAgent:
    index: int
    package_id: str
    object_id: str
    is_finished: bool


@dataclass
class AgentDatabase:
    agents: List[RegisteredAgent]


if settings.PRIVATE_KEY and settings.RPC_URL:
    sui_client = AsyncClient(SuiConfig.user_config(
        rpc_url=settings.RPC_URL,
        prv_keys=[settings.PRIVATE_KEY]
    ))
    print(f"Initialized SUI client with rpc url: {settings.RPC_URL}", flush=True)
else:
    sui_client = AsyncClient(SuiConfig.default_config())
    print(f"Initialized default local SUI client", flush=True)


async def main() -> None:
    # Static agent DB
    agent_database: AgentDatabase = AgentDatabase(
        agents=[]
    )
    while True:
        await _index_agents(settings.REGISTRY_OBJECT_ID, agent_database)
        for agent in agent_database.agents:
            if not agent.is_finished:
                is_success: bool = await _handle_agent_run(agent.package_id, agent.object_id)
                if is_success:
                    agent.is_finished = True
                    # is_finish_success = await _finish_agent_run(
                    #     registry_package_id=settings.REGISTRY_PACKAGE_ID,
                    #     registry_object_id=settings.REGISTRY_OBJECT_ID,
                    #     k=agent.index,
                    #     admin_cap_object_id=settings.ADMIN_CAP_OBJECT_ID,
                    # )
                    # if is_finish_success:
                    #     print(f"Successfully finished agent run with index {agent.index}", flush=True)
                    #     agent.is_finished = True
                    # else:
                    #     print(f"Failed to finish agent run with index {agent.index}", flush=True)
        time.sleep(10)


async def _index_agents(
    registry_object_id: str,
    agent_database: AgentDatabase,
):
    response = await sui_client.get_object(
        ObjectID(registry_object_id)
    )
    content = response.result_data.content
    registry_id = content.fields["agents"]["fields"]["id"]["id"]
    registry_response = await sui_client.execute(
        GetDynamicFields(ObjectID(registry_id))
    )
    for row in registry_response.result_data.data:
        entry = json.loads(row.name.replace("'", '"'))
        k = entry["value"]
        if not len([a for a in agent_database.agents if int(k) == a.index]):
            response = await sui_client.get_object(ObjectID(row.object_id))
            value: Dict = response.result_data.content.fields["value"]["fields"]
            agent_database.agents.append(
                RegisteredAgent(
                    index=int(k),
                    package_id=value["package_id"],
                    object_id=value["object_id"],
                    is_finished=value["is_finished"],
                )
            )


async def _finish_agent_run(
    registry_package_id: str,
    registry_object_id: str,
    k: int,
    admin_cap_object_id: str,
) -> bool:
    try:
        for_owner: SuiAddress = sui_client.config.active_address
        txn = AsyncTransaction(client=sui_client, initial_sender=for_owner)
        await txn.move_call(
            target=f"{registry_package_id}::oracle::finish_agent",
            arguments=[
                ObjectID(registry_object_id),
                SuiU64(k),
                ObjectID(admin_cap_object_id),
            ],
            type_arguments=[]
        )
        result = await txn.execute(
            gas_budget=100000000,
            use_gas_object=None
        )
        return result.is_ok() and result.result_data.succeeded
    except Exception as exc:
        print(exc, flush=True)
    return False


async def _handle_agent_run(
    package_id: str,
    agent_run_object_id: str,
) -> bool:
    agent_run: AgentRun = await _index_run(
        object_id=agent_run_object_id,
    )
    agent_run.llm_data.extend(
        await _index_llm_data(object_id=agent_run.llm_data_id)
    )
    tools = _get_tools(agent_run)
    openai_repository = OpenAiRepository(model="gpt-4")
    while not agent_run.is_finished:
        print(f"Agent run {agent_run_object_id} current state.", flush=True)
        print(agent_run, flush=True)

        output: Optional[OpenAiResult] = None
        if agent_run.llm_data[-1].type == "Function":
            function_input: Optional[Dict] = _get_formatted_function_input(agent_run.llm_data[-1].content)
            if function_input:
                output = await call_function_use_case.execute(function_input)
            else:
                output = await openai_repository.post_completion(
                    agent_run.llm_data[-1].content, tools)
        elif agent_run.llm_data[-1].type == "User":
            output = await openai_repository.post_completion(
                agent_run.llm_data[-1].content, tools)

        if output:
            await _iterate_agent(
                output=output.content,
                data_type=output.type,
                function_run_id=output.function_run_id,
                package_id=package_id,
                agent_run_object_id=agent_run.id,
            )
        else:
            print(f"Nothing to respond to for agent run {agent_run.id}")
        time.sleep(2)
        agent_run: AgentRun = await _index_run(
            object_id=agent_run_object_id,
        )
        agent_run.llm_data.extend(
            await _index_llm_data(object_id=agent_run.llm_data_id)
        )

    print("Agent run finished, final result: ", flush=True)
    print(agent_run.llm_data[-1].content, flush=True)
    # Naive success, failure is not really handled :)
    return True


async def _index_run(
    object_id: str,
) -> AgentRun:
    response = await sui_client.get_object(
        ObjectID(object_id)
    )
    fields = response.result_data.content.fields
    # No idea how to get the llm_data object ID here.. only the wrapper table ID
    return AgentRun(
        id=object_id,
        owner=fields["owner"],
        knowledge_base=fields["knowledge_base"],
        knowledge_base_description=fields["knowledge_base_description"],
        max_iterations=int(fields["max_iterations"]),
        is_finished=fields["is_finished"],
        llm_data_id=fields["llm_data"]["fields"]["id"]["id"],
        llm_data=[],
    )


async def _index_llm_data(
    object_id: str
) -> List[LlmData]:
    response = await sui_client.execute(
        GetDynamicFields(ObjectID(object_id))
    )
    table_object_ids: List[str] = [o.object_id for o in response.result_data.data]
    results: List[LlmData] = []
    for object_id in table_object_ids:
        object_result = await sui_client.get_object(
            ObjectID(object_id)
        )
        content = object_result.result_data.content.fields["value"]["fields"]
        results.append(
            LlmData(
                id=content["id"]["id"],
                index=content["index"],
                content=content["content"],
                type=content["type"],
                function_run_id=content["function_run_id"]
            )
        )
    return sorted(results, key=lambda x: x.index, reverse=False)


async def _iterate_agent(
    output: str,
    data_type: str,
    function_run_id: str,
    package_id: str,
    agent_run_object_id: str,
) -> bool:
    try:
        for_owner: SuiAddress = sui_client.config.active_address
        txn = AsyncTransaction(client=sui_client, initial_sender=for_owner)
        await txn.move_call(
            target=f"{package_id}::agent::iterate_agent",
            arguments=[
                output,
                data_type,
                function_run_id,
                ObjectID(agent_run_object_id),
            ],
            type_arguments=[]
        )
        result = await txn.execute(
            gas_budget=100000000,
            use_gas_object=None
        )
        return result.is_ok() and result.result_data.succeeded
    except Exception as exc:
        print(exc, flush=True)
    return False


def _get_formatted_function_input(prompt: str) -> Optional[Dict]:
    try:
        return json.loads(prompt)
    except:
        return None


def _get_tools(run: AgentRun) -> List[Dict]:
    tools = list(call_function_use_case.TOOLS)
    if run.knowledge_base:
        tool = vector_search_use_case.get_tool(run.knowledge_base, run.knowledge_base_description)
        tools.append(tool)
    return tools


if __name__ == '__main__':
    asyncio.run(main())
