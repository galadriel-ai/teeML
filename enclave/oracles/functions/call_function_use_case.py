import json
from typing import Dict
from typing import Optional

import requests

import settings
from repository.entities import OpenAiResult
from vector_search import vector_search_use_case


TOOLS = [
    {
        "type": "function",
        "function": {
            'name': 'web_search_json',
            'description': 'A search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events. Input should be a search query.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'description': 'search query to look up',
                        'type': 'string'
                    }
                },
                'required': ['query']
            }
        }
    }
]


async def execute(function_call: Dict) -> Optional[OpenAiResult]:
    formatted_arguments: Dict = _format_arguments(function_call)
    function_name = function_call.get("name")
    if function_name == "web_search_json" and formatted_arguments.get("query"):
        return _web_search(formatted_arguments["query"])
    elif function_name.startswith("vs_") and formatted_arguments.get("query"):
        return await _vector_store_search(function_name, formatted_arguments["query"])
    return None


def _format_arguments(function_call: Dict) -> Dict:
    try:
        return json.loads(function_call.get("arguments", {}))
    except:
        return {}


def _web_search(query: str) -> Optional[OpenAiResult]:
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": settings.SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "q": query
            }
        )
        return OpenAiResult(
            content=json.dumps(response.json()["organic"]),
            type="Function_result",
        )
    except Exception as e:
        print(f"Web search failed: {e}")
    return None


async def _vector_store_search(name: str, query: str) -> Optional[OpenAiResult]:
    try:
        cid = name.split("_")[-1]
        result = await vector_search_use_case.execute(cid, query)
        return OpenAiResult(
            content=result.content,
            type="Function_result",
            function_run_id=result.job_id,
        )
    except Exception as e:
        print(f"Vector store search failed: {e}")
    return None
