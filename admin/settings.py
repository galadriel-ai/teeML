from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
WEB3_RPC_URL = os.getenv("WEB3_RPC_URL")
