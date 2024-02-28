from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
REGISTRY_PACKAGE_ID = os.getenv("REGISTRY_PACKAGE_ID")
REGISTRY_OBJECT_ID = os.getenv("REGISTRY_OBJECT_ID")
ADMIN_CAP_OBJECT_ID = os.getenv("ADMIN_CAP_OBJECT_ID")
