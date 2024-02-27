from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

import settings
from repository.entities import OpenAiResult


class OpenAiRepository:

    def __init__(self, model: Literal["gpt-3.5-turbo", "gpt-4"]):
        self.model = model

    async def post_completion(self, prompt: str, tools: List[Dict]) -> Optional[OpenAiResult]:
        try:
            client = AsyncOpenAI(
                # This is the default and can be omitted
                api_key=settings.OPEN_AI_API_KEY,
            )

            chat_completion: ChatCompletion = await client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                tools=tools,
            )
            if tool_calls := chat_completion.choices[0].message.tool_calls:
                function_call_answer = tool_calls[0].function.json()
                print("Got OpenAI function_call answer", flush=True)
                return OpenAiResult(
                    content=function_call_answer,
                    type="Function",
                )
            answer = chat_completion.choices[0].message.content
            print("Got OpenAI answer", flush=True)
            return OpenAiResult(
                content=answer,
                type="Assistant",
            )
        except Exception as exc:
            print(f"OPENAI Exception: {exc}", flush=True)
