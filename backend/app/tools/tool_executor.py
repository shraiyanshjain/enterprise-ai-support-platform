import json

from app.tools.order_tools import get_order_status


class ToolExecutor:

    def execute(
        self,
        tool_name: str,
        arguments: str,
    ) -> dict:

        arguments_dict = json.loads(arguments)

        if tool_name == "get_order_status":
            return get_order_status(
                arguments_dict["order_id"]
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )