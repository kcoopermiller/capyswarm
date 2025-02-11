import json
from datetime import datetime
from typing import Tuple


def pretty_print_step(step, agent_name: str, color: Tuple[int, int, int]) -> None:
    """Print a step with colored output.

    Args:
        step: The step to print
        agent_name (str): Name of the agent
        color (Tuple[int, int, int]): RGB color tuple (r,g,b)
    """
    r, g, b = color
    ansi_color = f"38;2;{r};{g};{b}"

    if step.text:
        print(f"\033[{ansi_color}m{agent_name}\033[0m: {step.text}")

    if step.tool_calls:
        if len(step.tool_calls) > 1:
            print()
        for tool_call in step.tool_calls:
            name = tool_call.tool_name
            args_str = json.dumps(tool_call.args)
            print(f"\033[{ansi_color}m{name}\033[0m({args_str[1:-1]})")

    # Special handling for communicate tool calls
    if step.tool_results:
        for result in step.tool_results:
            if result.tool_name == "communicate":
                try:
                    for orch_step in result.result["orchestrator_response"]:
                        pretty_print_step(
                            orch_step,
                            "Orchestrator",
                            result.result["orchestrator_response_color"],
                        )
                except Exception:
                    print(
                        f"\033[{result.result['orchestrator_response_color']}mNo response from orchestrator\033[0m"
                    )


def debug_print(debug: bool, *args: str) -> None:
    if not debug:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    print(f"\033[97m[\033[90m{timestamp}\033[97m]\033[90m {message}\033[0m")
