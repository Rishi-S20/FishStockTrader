from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv
import os

load_dotenv()

client = TradingClient(os.getenv("API_KEY"), os.getenv("API_SECRET"), paper=True)
def is_tradeable(symbol):
    """Check if a stock is fractionable and a normal common stock."""
    if not symbol.isalpha():
        # Skip tickers with special characters like MS^I, BRK.B, etc.
        return False
    try:
        asset = client.get_asset(symbol)
        return asset.fractionable and asset.tradable
    except Exception:
        return False

def place_trade(symbol, amount=100):
    if not is_tradeable(symbol):
        print(f"{symbol} not tradeable — skipping.")
        return None

    order = MarketOrderRequest(
        symbol=symbol,
        notional=amount,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY  # fractional orders require DAY
    )
    result = client.submit_order(order)
    print(f"Order placed for ${amount} of {symbol} — Status: {result.status}")
    return result