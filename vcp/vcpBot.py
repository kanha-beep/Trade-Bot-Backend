import ta

# from server import symbols
from vcp.calculate_atr import calculate_atr

# from calculate_atr import calculate_atr
from vcp.detect_vcp import detect_vcp
from vcp.above_200ema import above_200ema
from vcp.rsi_50_crossover import rsi_50_crossover
from vcp.volume_dryness import volume_dryness
from vcp.two_fetch import fetch_data

# from vcp.all_symbols import ALL_SYMBOLS

from vcp.all_sym import get_nse_yfinance_symbols
from vcp.debug_vcp_stocks import debug_vcp_stocks
import time
from vcp.state import state
from fundamentals.get_fundamentals import get_fundamentals
from fundamentals.fundamentals_pass import fundamentals_pass

from vcp.vcp_variants import detect_vcp_all


def chunked(lst, size=40):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


fund_cache = {}


def vcpBot(symbols):
    vcp_stocks = []
    for batch_no, batch in enumerate(chunked(symbols, 40), start=1):
        print(f"Fetching data for batch {batch_no}...")
        df_all = fetch_data(batch)
        if df_all is None or df_all.empty:
            print("❌ Data fetch failed")
            time.sleep(5)
            continue
        for symbol in batch:
            try:
                # Some stocks fail to download
                if symbol not in fund_cache:
                    fund_cache[symbol] = get_fundamentals(symbol)

                if not fundamentals_pass(fund_cache[symbol]):
                    continue
                if symbol not in df_all:
                    continue
                df = df_all[symbol].copy()
                # print("updated stock: ", df)
                df.columns = df.columns.get_level_values(0)
                if df is None or df.empty:
                    continue
                # fund = get_fundamentals(symbol)
                df.dropna(inplace=True)
                # Need sufficient data (EMA + VCP)
                # print("updated stock: ", df)
                if len(df) < 200:
                    continue
                # Indicators
                df = calculate_atr(df)
                df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
                # df["EMA_200"] = ta.trend.ema_indicator(df["Close"], window=200)
                # Conditions
                closes = df["Close"].tolist()
                highs = df["High"].tolist()
                lows = df["Low"].tolist()
                volumes = df["Volume"].tolist()
                vcpS = detect_vcp_all(df)
                # vcp = detect_vcp(df)
                vcp = detect_vcp(close=closes, high=highs, low=lows, volume=volumes)
                # print("is vcp: ", vcp, "vap values: " + vcpS)
                print(f"{symbol} is vcp: {vcp} | vcp values: {vcpS}")
                rsi_ok = rsi_50_crossover(df)
                vol_ok = volume_dryness(df)
                # trend_ok = (df.tail(22)["Close"] > df.tail(22)["EMA_200"]).all()
                trend_ok = above_200ema(df, days=30)
                # print("above 200ema: ", trend_ok)
                # print(
                #     f"{symbol} | "
                #     f"VCP={vcp} | "
                #     f"RSI={rsi_ok} | "
                #     f"VOL={vol_ok} | "
                #     f"EMA200={trend_ok}"
                # )

                signals = []
                if vcpS:
                    # signals.append("VCP")
                    signals.extend(vcpS)
                if trend_ok:
                    signals.append("EMA200")
                if vol_ok:
                    signals.append("VOLUME")
                if vcp and vol_ok and trend_ok:
                    print(f"🔥 {symbol} IS VCP")
                    vcp_stocks.append(
                        {
                            "symbol": symbol,
                            "signals": signals.copy(),
                            "indicators": {
                                "ema200": trend_ok,
                                "rsi": rsi_ok,
                                "volume": vol_ok,
                            },
                            "price": float(df["Close"].iloc[-1]),
                        }
                    )
                    # vcp_stocks.append(symbol)
                    # state["results"].clear()
                    state["results"] = list(vcp_stocks)
                    # print("1. state: ", state["results"])
                    # state["results"].extend(vcp_stocks)
                    # print("2. state: ", state["results"])
                    state["last_run"] = time.time()
                # state["last_run"] = time.time()
            except Exception as e:
                print(f"⚠️ Error in {symbol}: {e}")
        # state["results"].clear()
        # state["results"].extend(vcp_stocks)
        # state["last_run"] = time.time()
    time.sleep(2)
    print("state: ", state)
    return vcp_stocks


if __name__ == "__main__":
    ALL_SYMBOLS = get_nse_yfinance_symbols()
    print("Total NSE Stocks:", len(ALL_SYMBOLS))
    results = vcpBot(ALL_SYMBOLS)
    res = debug_vcp_stocks(ALL_SYMBOLS)
    print("Debug VCP stocks:", res)
    print("SCAN SIZE:", len(state["results"]))
    print("\n✅ FINAL VCP STOCKS:")
    print(results)
