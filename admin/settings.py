from typing import Dict

from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

CHAIN_ID = os.getenv("CHAIN_ID", "")
WEB3_RPC_URL = os.getenv("WEB3_RPC_URL", "")
ORACLE_ADDRESS = os.getenv("ORACLE_ADDRESS", "")
ORACLE_ABI_PATH = os.getenv("ORACLE_ABI_PATH", "")

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "galadriel-assets")
BEARLY_API_KEY = os.getenv("BEARLY_API_KEY", "")
NFT_STORAGE_API_KEY = os.getenv("NFT_STORAGE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def get_dot_env() -> Dict:
    return {
        "ENVIRONMENT": "production",
        "OPEN_AI_API_KEY": OPEN_AI_API_KEY,
        "SERPER_API_KEY": SERPER_API_KEY,
        "CHAIN_ID": CHAIN_ID,
        "WEB3_RPC_URL": WEB3_RPC_URL,
        "ORACLE_ADDRESS": ORACLE_ADDRESS,
        "ORACLE_ABI_PATH": "/app/oracles/ChatOracle.json",
        "GCS_BUCKET_NAME": GCS_BUCKET_NAME,
        "BEARLY_API_KEY": BEARLY_API_KEY,
        "NFT_STORAGE_API_KEY": NFT_STORAGE_API_KEY,
        "GROQ_API_KEY": GROQ_API_KEY,
    }
