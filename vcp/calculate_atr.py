# import pandas as pd


# def calculate_atr(df, period=14):
#     high_low = df['High'] - df['Low']
#     high_close = abs(df['High'] - df['Close'].shift())
#     low_close = abs(df['Low'] - df['Close'].shift())
#     ranges = pd.concat([high_low, high_close, low_close], axis=1)
#     true_range = ranges.max(axis=1)
#     df['ATR'] = true_range.rolling(period).mean()
#     return
import pandas as pd

def calculate_atr(df, period=14):
    if not {"High", "Low", "Close"}.issubset(df.columns):
        return df
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    true_range = pd.concat(
        [high_low, high_close, low_close], axis=1
    ).max(axis=1)
    df = df.copy()
    df["ATR"] = true_range.rolling(period).mean()
    return df
