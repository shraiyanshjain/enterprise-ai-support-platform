def get_order_status(order_id: str) -> dict:
    """
    Get the current status of an order.
    """

    orders = {
        "1001": {
            "order_id": "1001",
            "status": "SHIPPED",
            "estimated_delivery": "2026-09-05",
        },
        "1002": {
            "order_id": "1002",
            "status": "PROCESSING",
            "estimated_delivery": "2026-09-07",
        },
        "1003": {
            "order_id": "1003",
            "status": "DELIVERED",
            "estimated_delivery": "2026-09-01",
        },
    }

    order = orders.get(order_id)

    if not order:
        return {
            "order_id": order_id,
            "status": "NOT_FOUND",
        }

    return order