from app.core.openai_client import client


class AIService:

    def generate_response(
        self,
        messages: list[dict],
    ) -> str:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        return response.choices[0].message.content

    def generate_response_with_tools(
         self,
         messages: list[dict],
         tools: list[dict],
    ):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

        return response