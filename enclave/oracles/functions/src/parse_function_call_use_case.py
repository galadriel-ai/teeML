from typing import Tuple


def execute(function_input: str) -> Tuple[str, Tuple[str]]:
    name = function_input.split("(")[0]
    params = [a.strip() for a in function_input.split("(")[1].split(")")[0].split(",")]
    formatted_params = []
    for p in params:
        if len(p) and p[0] == '"':
            p = p[1:]
        if len(p) and p[-1] == '"':
            p = p[:-1]
        formatted_params.append(p)
    return name, tuple(formatted_params)
