from dataclasses import dataclass
from typing import Literal


@dataclass
class OpenAiResult:
    content: str
    type: Literal["User", "Assistant", "Function", "Function_result"]
    function_run_id: str = ""
