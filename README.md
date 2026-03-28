# Binance Futures Testnet Trading Bot

A Python command-line application designed to place orders securely on the Binance Futures Testnet (USDT-M). This repository provides a scalable structure, separating UI/CLI components from internal API logic, with dedicated configuration layers.

## Features Enforced

1. **Market Orders**: Directly open positions at prevailing market rates.
2. **Limit Orders**: Restrict entries to specific price zones.
3. **Stop-Market Orders (Bonus)**: Trigger an automatic market entry/exit based on dynamic price actions.
4. **Enhanced UI (Bonus)**: Incorporates `typer` and `rich`, providing colorful summary tables and error traces on the console.
5. **Robust Error Handling**: Specific intercepts for general logic bugs as well as parsed `BinanceAPIException` streams.
6. **File Logging**: Prevents terminal bloat; background records request configurations, execution timelines, and failure stacks into `trading_bot.log`. 

## Setup Steps

**1. Clone the environment and navigate inside**
```bash
cd trading_bot
```

**2. Virtual Environment setup (Recommended)**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On MacOS/Linux
source venv/bin/activate
```

**3. Install Dependencies from Text File**
```bash
pip install -r requirements.txt
```

**4. Binance API Keys Setup**
You need testnet credentials from [Binance Futures Testnet](https://testnet.binancefuture.com). Let the bot authenticate accurately:
1. Rename `.env.example` to `.env`.
2. Edit `.env` to input your API parameters:
```env
BINANCE_API_KEY=your_actual_testnet_key
BINANCE_API_SECRET=your_actual_testnet_secret
```

## How to run examples

Use the main `cli.py` file to drive actions.

```bash
# General Syntax Check
python cli.py --help

# Execute a MARKET Order (BUY BTCUSDT size 0.005)
python cli.py market BTCUSDT BUY 0.005

# Execute a MARKET Order (SELL BTCUSDT size 0.001)
python cli.py market BTCUSDT SELL 0.001

# Execute a LIMIT Order (BUY ADAUSDT size 100 at 0.40)
python cli.py limit ADAUSDT BUY 100 0.40

# Execute a STOP_MARKET Order (SELL ETHUSDT size 0.01 at stop_price 1800) -- (BONUS)
python cli.py stop-market ETHUSDT SELL 0.01 1800
```

## Logging Trace
After running your application, check the `trading_bot.log` file automatically created at the project root for chronological data mapping request sequences, testnet parameters, and successful/failure responses.

## Assumptions
- Designed around the exact URL `https://testnet.binancefuture.com` exclusively through testnet configurations exposed in Python-Binance initialization.
- Assets are traded as purely isolated/cross margin default based on the raw account state since specific leverage adjustments were left out of core requirements.
- Uses Standard `USDT-M` derivatives, ignoring Coin-M setups.
