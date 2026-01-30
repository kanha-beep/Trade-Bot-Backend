# vcp/trade_engine.py
from vcp.two_fetch import fetch_data
from vcp.calculate_atr import calculate_atr
from vcp.breakout_confirmation import breakout_confirmation
from vcp.position_size import position_size

def generate_trade(symbol, capital=100000):
    df = fetch_data([symbol])[symbol]
    df = calculate_atr(df)
    df.dropna(inplace=True)

    if not breakout_confirmation(df):
        return None

    entry = df["Close"].iloc[-1]
    stop = df["Low"].tail(10).min()
    qty = position_size(capital, entry, stop)

    if qty == 0:
        return None

    return {
        "symbol": symbol,
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "qty": qty
    }