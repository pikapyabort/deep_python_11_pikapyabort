import json
from typing import Callable


def default_callback(x: str, y: str) -> None:
    print(f'key = "{x}", token = "{y}"')


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    if not required_keys or not tokens:
        return
    if callback is None:
        callback = default_callback
    data = json.loads(json_str)
    for req_key in required_keys:
        if req_key in data:
            value = data[req_key]
            for token in tokens:
                if token.lower() in value.lower():
                    callback(req_key, token)
