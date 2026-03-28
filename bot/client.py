import os
from binance.client import Client
from dotenv import load_dotenv
from .logging_config import logger

# Load environment variables
load_dotenv()

def get_binance_client() -> Client:
    """
    Initializes and returns a Binance client connected to the Futures Testnet.
    Credentials must be set in the .env file or environment variables.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Binance API credentials not found in environment.")
        raise ValueError(
            "API credentials missing. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file."
        )

    logger.info("Initializing Binance Client with Futures Testnet configuration.")
    try:
        # We enforce testnet=True so it routes to https://testnet.binancefuture.com
        client = Client(api_key, api_secret, testnet=True)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Binance Client: {e}")
        raise
