"""
curl -v https://api.openai.com/v1/chat/completions   \
  -H "Content-Type: application/json"   \
  -H "Authorization: Bearer $OPENAI_API_KEY"   \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
      },
      {
        "role": "user",
        "content": "Compose a poem that explains the concept of recursion in programming."
      }
    ]
  }'
"""
import os

import requests

print("\n=== Making OPENAI call ===")
URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY", ""),
}
DATA = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You a simple greeter"
        },
        {
            "role": "user",
            "content": "Greet me"
        }
    ]
}
result = requests.post(URL, headers=HEADERS, json=DATA)
print("Result from OPENAI:", result)
print("Result from OPENAI:", result.json())
print("=== OPENAI Call done ===\n")
