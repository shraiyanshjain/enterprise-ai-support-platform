class PromptBuilder:

    def build(
        self,
        question: str,
        documents: list[dict],
        history: list[dict] | None = None,
    ) -> list[dict]:

        context_parts = []

        for document in documents:
            context_parts.append(
                f"Source: {document['source']}\n"
                f"Content: {document['text']}"
            )

        context = "\n\n".join(context_parts)

        if not context:
            context = "No relevant information was found in the knowledge base."

        system_prompt = f"""
You are an enterprise customer support assistant.

Answer the user's question using ONLY the provided knowledge base context.

If the answer cannot be found in the context, say:
"I don't have enough information in the knowledge base to answer that."

Do not invent policies, dates, prices, or other facts.

Be concise and helpful.

Knowledge base context:

{context}
""".strip()

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        if history:
            messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        return messages