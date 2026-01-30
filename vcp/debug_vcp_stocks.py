from vcp.two_fetch import fetch_data
from vcp.indicators import add_indicators
from vcp.detect_vcp import detect_vcp
from vcp.rsi_50_crossover import rsi_50_crossover
from vcp.volume_dryness import volume_dryness
from vcp.above_200ema import above_200ema
from vcp.state import state
def debug_vcp_stocks(symbols):
    vcp_stocks = []
    df_all = fetch_data(symbols)

    for symbol in symbols:
        try:
            if symbol not in df_all:
                continue

            df = df_all[symbol].copy()
            df.columns = df.columns.get_level_values(0)
            df.dropna(inplace=True)

            if len(df) < 200:
                continue

            df = add_indicators(df)

            is_vcp = (
                detect_vcp(df)
                and rsi_50_crossover(df)
                and volume_dryness(df)
                and above_200ema(df)
            )

            print(
                f"DEBUG | "
                f"{symbol} | "
                f"VCP={detect_vcp(df)} | "
                f"RSI={rsi_50_crossover(df)} | "
                f"VOL={volume_dryness(df)} | "
                f"EMA200={above_200ema(df)}"
            )
            print("SCAN SIZE:", len(state["results"]))

            if is_vcp:
                vcp_stocks.append(symbol)

        except Exception as e:
            print(f"Error in {symbol}: {e}")

    return vcp_stocks
