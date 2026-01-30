import pandas as pd
import ta


def add_indicators(df):
    # ATR
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    # RSI
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    # EMA 200
    df["EMA_200"] = ta.trend.ema_indicator(df["Close"], window=200)

    return df
