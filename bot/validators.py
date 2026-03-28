def validate_symbol(symbol: str) -> str:
    # Ensures symbol is uppercase.
    return symbol.upper()

def validate_side(side: str) -> str:
    # Ensures side is either BUY or SELL.
    side_upper = side.upper()
    if side_upper not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    return side_upper

def validate_quantity(qty: float) -> float:
    # Ensures quantity is strictly positive.
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return qty

def validate_price(price: float, order_type: str) -> float:
    """
    Ensures price is greater than 0 if type requires it.
    If it's a LIMIT order, price is required and must be validated.
    """
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price must be specified and > 0 for LIMIT orders.")
    return price
