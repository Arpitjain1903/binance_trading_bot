from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance.enums import *
from typing import Dict, Any, Optional

from .logging_config import logger
from .client import get_binance_client

def place_futures_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Submits an order to the Binance Futures testnet.

    Supported basic types: MARKET, LIMIT.
    Bonus feature added: STOP_MARKET.

    Returns the raw dictionary response from Binance, containing orderId, status, executedQty, etc.
    """
    client = get_binance_client()

    log_msg = f"Requesting {order_type} {side} order for {quantity} {symbol}"
    if price:
        log_msg += f" at price {price}"
    if stop_price:
        log_msg += f" with stop {stop_price}"
    logger.info(log_msg)

    # Base parameters required for all orders
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    try:
        if order_type == 'LIMIT':
            params['timeInForce'] = TIME_IN_FORCE_GTC
            params['price'] = price
            logger.info(f"Submitting LIMIT parameters: {params}")
            response = client.futures_create_order(**params)

        elif order_type == 'MARKET':
            logger.info(f"Submitting MARKET parameters: {params}")
            response = client.futures_create_order(**params)

        elif order_type == 'STOP_MARKET':
            params['stopPrice'] = stop_price
            logger.info(f"Submitting STOP_MARKET parameters: {params}")
            response = client.futures_create_order(**params)

        else:
            raise ValueError(f"Order type {order_type} is not supported by this bot.")

        logger.info(f"Order Success - Response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception occurred: {e.status_code} - {e.message}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: Network error or invalid request parameters - {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
