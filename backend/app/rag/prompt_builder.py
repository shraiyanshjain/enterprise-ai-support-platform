class PromptBuilder:

    def build(
        self,
        question: str,
        documents: list[dict],
    ) -> list[dict]:

        context_parts = []

        for document in documents:
            context_parts.append(
                f"Source: {document['source']}\n"
                f"Content: {document['text']}"
            )

        context = "\n\n".join(context_parts)

        system_prompt = """
You are an enterprise customer support assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the knowledge base to answer that."

Do not invent policies, dates, prices, or other facts.

Be concise and helpful.
""".strip()

        user_prompt = f"""
Context:

{context}

User question:

{question}
""".strip()

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]