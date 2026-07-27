import uuid


def generate_transaction_id():
    return str(uuid.uuid4())


def generate_order_number():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"