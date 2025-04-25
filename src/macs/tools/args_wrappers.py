import json

from typing import Callable, Union, Dict


def structured_tool_wrapper(func: Callable) -> Callable[[Union[str, Dict]], str]:

    def wrapped(input_data: Union[str, Dict]) -> str:
        if isinstance(input_data, str):
            input_data = input_data.strip()

            if input_data.startswith("{") and input_data.endswith("}"):
                try:
                    input_data = json.loads(input_data)
                except json.JSONDecodeError:
                    return func(input=input_data)
            else:
                return func(input=input_data)

        if isinstance(input_data, dict):
            return func(**input_data)
        raise ValueError(f"Unsupported input type: {type(input_data)}")

    return wrapped
