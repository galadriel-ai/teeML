import asyncio
import argparse
from vector_search.src import query_on_bacalhau_use_case
from vector_search.src.entities import VectorSearchResult


def get_tool(cid: str, description: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": f"vs_{cid}",
            "description": f"Retrieves content from a vector database containing {description}. Use this function to answer any user questions related to {description}.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "description": f"A question related to {description}",
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    }


async def execute(cid: str, query: str) -> VectorSearchResult:
    return await query_on_bacalhau_use_case.execute(cid, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="The query")
    parser.add_argument("--cid", type=str, default="bafybeihp3lwjldg53s2vqopkfmffsw5elj3bglba43gdh5jslmprgmmtcm", help="Database CID")
    args = parser.parse_args()
    print(asyncio.run(execute(args.cid, args.query)))
