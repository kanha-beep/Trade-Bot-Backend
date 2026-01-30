import ta
from vcp.calculate_atr import calculate_atr

def strategy(df):
    # print("Running strategy 3")
    df["ema4"] = ta.trend.ema_indicator(df["Close"], 4)
    df["ema9"] = ta.trend.ema_indicator(df["Close"], 9)
    df["ema20"] = ta.trend.ema_indicator(df["Close"], 20)
    df["ema50"] = ta.trend.ema_indicator(df["Close"], 50)
    df["ema100"] = ta.trend.ema_indicator(df["Close"], 100)
    df["ema200"] = ta.trend.ema_indicator(df["Close"], 200)
    df["macd"] = ta.trend.macd(df["Close"], 12, 26, 9)
    df["rsi"] = ta.momentum.rsi(df["Close"], 14)
    # 2️⃣ RSI Moving Average (RSI-based MA)
    df["rsi_ma"] = df["rsi"].rolling(window=14).mean()
    # 3️⃣ RSI Bands (Static Levels)
    df["rsi_upper"] = 80
    df["rsi_mid"] = 50
    df["rsi_lower"] = 20
    # RSI crosses ABOVE lower band (20)
    df["rsi_cross_above_20"] = (df["rsi"].shift(1) < 20) & (df["rsi"] >= 20)
    # RSI crosses BELOW upper band (80)
    df["rsi_cross_below_80"] = (df["rsi"].shift(1) > 80) & (df["rsi"] <= 80)
    # RSI crosses ABOVE its MA (Bullish)
    df["rsi_cross_above_ma"] = (df["rsi"].shift(1) < df["rsi_ma"].shift(1)) & (
        df["rsi"] >= df["rsi_ma"]
    )
    # RSI crosses BELOW its MA (Bearish)
    df["rsi_cross_below_ma"] = (df["rsi"].shift(1) > df["rsi_ma"].shift(1)) & (
        df["rsi"] <= df["rsi_ma"]
    )
    # Buy Signal:
    # RSI exits oversold AND confirms momentum
    df["buy_signal"] = df["rsi_cross_above_20"] & df["rsi_cross_above_ma"]
    # Sell Signal:
    # RSI exits overbought AND loses momentum
    df["sell_signal"] = df["rsi_cross_below_80"] & df["rsi_cross_below_ma"]
    df.dropna(inplace=True)
    # Latest values
    ema4 = df["ema4"].iloc[-1]
    ema9 = df["ema9"].iloc[-1]
    ema20 = df["ema20"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]
    ema100 = df["ema100"].iloc[-1]
    ema200 = df["ema200"].iloc[-1]
    rsi = df["rsi"].iloc[-1]
    rsi_ma = df["rsi_ma"].iloc[-1]
    bullish_trend = ema9 > ema20
    ema4_prev = df["ema4"].iloc[-2]
    ema9_prev = df["ema9"].iloc[-2]
    ema20_prev = df["ema20"].iloc[-2]
    ema4_cross_9 = ema4_prev < ema9_prev and ema4 > ema9
    ema4_cross_20 = ema4_prev < ema20_prev and ema4 > ema20
    ema9_cross_20 = ema9_prev < ema20_prev and ema9 > ema20
    rsi_prev = df["rsi"].iloc[-2]
    rsi_ma_prev = df["rsi_ma"].iloc[-2]
    rsi_cross_ma = rsi_prev < rsi_ma_prev and rsi > rsi_ma
    if (
        bullish_trend
        and ema4_cross_9
        and ema4_cross_20
        and ema9_cross_20
        and rsi_cross_ma
    ):
        return "BUY"
    bearish_trend = ema9 < ema20
    ema4_cross_9 = ema4_prev > ema9_prev and ema4 < ema9
    ema4_cross_20 = ema4_prev > ema20_prev and ema4 < ema20
    ema9_cross_20 = ema9_prev > ema20_prev and ema9 < ema20
    rsi_cross_ma = rsi_prev > rsi_ma_prev and rsi < rsi_ma
    if (
        bearish_trend
        and ema4_cross_9
        and ema4_cross_20
        and ema9_cross_20
        and rsi_cross_ma
    ):
        return "SELL"
    return "HOLD"
