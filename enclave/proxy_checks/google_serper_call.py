async def execute() -> (bool, str):
    try:
        import aiohttp
        import settings
        import json

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": settings.SERPER_API_KEY,
                    "Content-Type": "application/json",
                },
                json={"q": "Capital of Tallinn"},
            ) as response:
                response.raise_for_status()
                data = await response.json()
                print("result:", json.dumps(data["organic"][0]))
        return True, ""
    except Exception as exc:
        return False, str(exc)