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