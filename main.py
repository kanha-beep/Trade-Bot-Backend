import time as t
import logging
from one_market_open import market_open
from two_fetch import fetch_data
from three_strategy_indicators import strategy
from four_risk_mgmt import risk_ok
from five_start_trade import state, can_trade
import seven_log
from five_one_stop_loss import get_stop_loss
from datetime import datetime
import pytz
from symbols import ALL_SYMBOLS

IST = pytz.timezone("Asia/Kolkata")
SYMBOLS = ALL_SYMBOLS

while True:
    print("start bot: ", datetime.now(IST).strftime("%d-%m-%Y %H:%M:%S"))
    try:
        # if not market_open():
        #     print("Closed")
        #     t.sleep(10)
        #     continue
        logging.info("Bot started")
        df_all = fetch_data(SYMBOLS)
        for SYMBOL in SYMBOLS:
            # print("start symbol: ", SYMBOL)
            # print("1. ", df_all)
            df = df_all[SYMBOL].dropna()
            # print("2. df: ", df)
            df.columns = df.columns.get_level_values(0)
            # print("3. df: ", df.columns)
            if df.empty or len(df) < 2:
                print(f"⚠️ Skipping {SYMBOL} — no usable data")
                continue
            last_close = df["Close"].iloc[-1]
            last_high = df["High"].iloc[-1]
            last_low = df["Low"].iloc[-1]
            last_open = df["Open"].iloc[-1]
            last_vol = df["Volume"].iloc[-1]
            # print(f"4. {SYMBOL} : {last_close}")
            if df is None or df.empty:
                logging.error("Data fetch failed")
                t.sleep(10)
                continue
            try:
                # print("6. copy: ", df)
                signal = strategy(df)
                # print("5. signal:", signal)
            except Exception as e:
                print("❌ Strategy error for", SYMBOL)
                print(e)
                continue
            # print("5. signal: ", signal)
            # print(f"What to do ===> {SYMBOL}, {signal}")
            price = df.Close.iloc[-1]
            # print("price: ", price)
            # 3% SL
            sl_3 = get_stop_loss(price, sl_pct=3)
            # print("stop loss 3 :", sl_3)
            # 5% SL
            sl_5 = get_stop_loss(price, sl_pct=5)
            # print("stop loss 5 :", sl_5)
            # sl = price * 0.98
            if signal == "BUY" and can_trade(SYMBOL):
                qty = risk_ok(price, sl_3)
                if qty > 0:
                    logging.info(f"BUY {SYMBOL} @ {price} qty={qty}")
                    print(f"BUY ALERT → {SYMBOL}")
                    state[SYMBOL] = True
                else:
                    logging.warning(f"Risk failed for {SYMBOL}")
            if signal == "SELL" and state.get(SYMBOL):
                logging.info(f"SELL {SYMBOL} @ {price}")
                print("SELL ALERT")
                state[SYMBOL] = False
        t.sleep(10)
    except Exception as e:
        logging.error(str(e))
        t.sleep(10)
