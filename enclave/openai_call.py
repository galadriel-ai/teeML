
import settings

import requests

print("\n=== Making OPENAI call ===")
URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + settings.OPEN_AI_API_KEY,
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
