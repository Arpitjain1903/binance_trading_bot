import typer
import json
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price
from bot.orders import place_futures_order
from bot.logging_config import logger

app = typer.Typer(help="CLI tool to place orders on Binance Futures Testnet [USDT-M]")
console = Console()

def display_summary(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """
    Displays the request summary table to the user.
    """
    table = Table(title="Order Request Summary", title_style="bold cyan")
    table.add_column("Parameter", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))
        
    console.print(table)


def display_response(response: dict):
    """
    Displays the response details from Binance in a clean Rich table.
    """
    table = Table(title="Order Response Details", title_style="bold green")
    table.add_column("Field", style="green", no_wrap=True)
    table.add_column("Value", style="yellow")

    keys_to_display = ["orderId", "status", "symbol", "side", "type", "executedQty", "avgPrice", "origQty", "price"]
    for key in keys_to_display:
        val = response.get(key, "N/A")
        table.add_row(key, str(val))
        
    console.print(table)
    console.print("[bold green]✅ Order placed successfully![/bold green]")

def handle_errors(e: Exception):
    """
    Displays structured error traces gracefully visually.
    """
    if isinstance(e, BinanceAPIException):
        console.print(f"[bold red]❌ Binance API Error:[/bold red] {e.status_code} - {e.message}")
    elif isinstance(e, BinanceRequestException):
        console.print(f"[bold red]❌ Network/Request Error:[/bold red] {e}")
    elif isinstance(e, ValueError):
        console.print(f"[bold red]❌ Validation Error:[/bold red] {e}")
    else:
        console.print(f"[bold red]❌ Unexpected Error:[/bold red] {e}")

@app.command("market")
def run_market(
    symbol: str = typer.Argument(..., help="Trading Pair Symbol (e.g. BTCUSDT)"),
    side: str = typer.Argument(..., help="Direction of Trade (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity sizes for the traded asset")
):
    """
    Places a MARKET order on the Binance Futures Testnet.
    """
    try:
        # Validate Input
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_qty = validate_quantity(quantity)

        display_summary(v_symbol, v_side, "MARKET", v_qty)

        # Place the order
        response = place_futures_order(
            symbol=v_symbol,
            side=v_side,
            order_type="MARKET",
            quantity=v_qty
        )
        
        display_response(response)

    except Exception as e:
        handle_errors(e)


@app.command("limit")
def run_limit(
    symbol: str = typer.Argument(..., help="Trading Pair Symbol (e.g. BTCUSDT)"),
    side: str = typer.Argument(..., help="Direction of Trade (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity sizes for the traded asset"),
    price: float = typer.Argument(..., help="At what price point should the order be filled?")
):
    """
    Places a LIMIT order on the Binance Futures Testnet.
    """
    try:
        # Validate Input
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_qty = validate_quantity(quantity)
        v_price = validate_price(price, "LIMIT")

        display_summary(v_symbol, v_side, "LIMIT", v_qty, price=v_price)

        # Place the order
        response = place_futures_order(
            symbol=v_symbol,
            side=v_side,
            order_type="LIMIT",
            quantity=v_qty,
            price=v_price
        )
        
        display_response(response)

    except Exception as e:
        handle_errors(e)
        
@app.command("stop-market")
def run_stop_market(
    symbol: str = typer.Argument(..., help="Trading Pair Symbol (e.g. BTCUSDT)"),
    side: str = typer.Argument(..., help="Direction of Trade (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity sizes for the traded asset"),
    stop_price: float = typer.Argument(..., help="At what price should the market order be triggered?")
):
    """
    Places a STOP_MARKET order on the Binance Futures Testnet. (Bonus Feature)
    """
    try:
        # Validate Input
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_qty = validate_quantity(quantity)
        
        if stop_price <= 0:
            raise ValueError("stop_price must be > 0.")

        display_summary(v_symbol, v_side, "STOP_MARKET", v_qty, stop_price=stop_price)

        # Place the order
        response = place_futures_order(
            symbol=v_symbol,
            side=v_side,
            order_type="STOP_MARKET",
            quantity=v_qty,
            stop_price=stop_price
        )
        
        display_response(response)

    except Exception as e:
        handle_errors(e)

if __name__ == "__main__":
    app()
