import json

from app.services.ai_service import AIService
from app.tools.tool_definitions import ORDER_STATUS_TOOL
from app.tools.tool_executor import ToolExecutor


class ToolCallingService:

    def __init__(
        self,
        ai_service: AIService,
        tool_executor: ToolExecutor,
    ):
        self.ai_service = ai_service
        self.tool_executor = tool_executor

    def process(
        self,
        messages: list[dict],
    ) -> str:

        tools = [
            ORDER_STATUS_TOOL
        ]

        response = self.ai_service.generate_response_with_tools(
            messages,
            tools,
        )

        assistant_message = response.choices[0].message

        # No tool call -> normal response
        if not assistant_message.tool_calls:
            return assistant_message.content

        # Add assistant's tool-call message
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in assistant_message.tool_calls
                ],
            }
        )

        # Execute each requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = self.tool_executor.execute(
                tool_name,
                arguments,
            )

            # Add tool result to conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        # Ask OpenAI for final answer
        final_response = self.ai_service.generate_response_with_tools(
            messages,
            tools,
        )

        return final_response.choices[0].message.content