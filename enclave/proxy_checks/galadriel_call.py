from web3.types import BlockData


async def execute() -> (bool, str):
    try:
        from web3 import AsyncWeb3
        import settings
        web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_RPC_URL))
        result: BlockData = await web3_client.eth.get_block('latest')
        print("result: latest block numer:", result.number)
        return True, ""
    except Exception as exc:
        return False, str(exc)
