ORDER_STATUS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Get the current status and estimated delivery date of a customer order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The customer's order ID.",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
}