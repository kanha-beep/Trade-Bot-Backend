from vcp.generate_trade import generate_trade
import time
from vcp.state import state
def trade_engine_loop():
    while True:
        trades = []

        for symbol in state.get("results", []):
            try:
                trade = generate_trade(symbol)
                if trade:
                    trades.append(trade)
            except Exception as e:
                print("Trade engine error:", e)

        state["trades"] = trades
        time.sleep(60)  # check breakout every candle
