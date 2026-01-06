import time as t
import logging
from one_market_open import market_open
from two_fetch import fetch_data
from three_strategy_indicators import strategy
from four_risk_mgmt import risk_ok
from five_start_trade import state, can_trade
import seven_log
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
SYMBOLS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "COALINDIA.NS"]


def bot():
    while True:
        print("start bot: ", datetime.now(IST).strftime("%d-%m-%Y %H:%M:%S"))
        try:
            if not market_open():
                print("Closed")
                t.sleep(5)
                continue
            logging.info("Bot started")
            df_all = fetch_data(SYMBOLS)
            for SYMBOL in SYMBOLS:
                # print("start symbol: ", SYMBOL)
                df = df_all[SYMBOL].dropna()
                df.columns = df.columns.get_level_values(0)
                last_close = df["Close"].iloc[-1]
                last_high = df["High"].iloc[-1]
                last_low = df["Low"].iloc[-1]
                last_open = df["Open"].iloc[-1]
                last_vol = df["Volume"].iloc[-1]
                print(f"{SYMBOL} : {last_close}")
                if df is None or df.empty:
                    logging.error("Data fetch failed")
                    t.sleep(5)
                    continue
                signal = strategy(df)
                print(SYMBOL, signal)
                price = df.Close.iloc[-1]
                state[SYMBOL] = {
                    "signal": signal,
                    "price": price,
                    "in_trade": state.get(SYMBOL, {}).get("in_trade", False),
                }
                sl = price * 0.98
                if signal == "BUY" and not state.get(SYMBOL, {}).get("in_trade"):
                    qty = risk_ok(price, sl)
                    if qty > 0:
                        state[SYMBOL] = {
                            "in_trade": True,
                            "entry": price,
                            "sl": price * 0.98,
                            "target": price * 1.04,
                            "qty": qty,
                        }
                    else:
                        logging.warning(f"Risk failed for {SYMBOL}")
                if state.get(SYMBOL, {}).get("in_trade"):
                    entry = state[SYMBOL]["entry"]
                    sl = state[SYMBOL]["sl"]
                    target = state[SYMBOL]["target"]
                    # Stop-loss hit
                    if price <= sl:
                        print(f"SL HIT → {SYMBOL}")
                        logging.info(f"SELL {SYMBOL} SL @ {price}")
                        state[SYMBOL]["in_trade"] = False
                        # Target hit
                    elif price >= target:
                        print(f"TARGET HIT → {SYMBOL}")
                        logging.info(f"SELL {SYMBOL} TARGET @ {price}")
                        state[SYMBOL]["in_trade"] = False

                    # Profit booking (EMA-based trailing)
                    elif price > entry and df.ema9.iloc[-1] < df.ema20.iloc[-1]:
                        print(f"PROFIT BOOK → {SYMBOL}")
                        logging.info(f"SELL {SYMBOL} PROFIT @ {price}")
                        state[SYMBOL]["in_trade"] = False
            t.sleep(5)
        except Exception as e:
            logging.error(str(e))
            t.sleep(5)
