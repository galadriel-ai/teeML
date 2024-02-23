from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
