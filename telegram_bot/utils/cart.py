from utils.texts import TEXTS


def build_cart_text(cart: list, language: str) -> str:
    if not cart:
        return TEXTS[language]["cart_empty"]

    text = f"{TEXTS[language]['your_cart']}\n\n"

    total = 0

    for item in cart:
        subtotal = item["quantity"] * item["price"]
        total += subtotal

        text += (
            f"📦 {item['name']}\n"
            f"➖ {item['quantity']} × {item['price']} = {subtotal} UZS\n\n"
        )

    text += f"💵 Total: {total} UZS"

    return text
