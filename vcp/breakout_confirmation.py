def breakout_confirmation(df, lookback=20):
    if len(df) < lookback + 1:
        return False

    pivot_high = df["High"].tail(lookback).max()
    close = df["Close"].iloc[-1]

    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    vol_expansion = df["Volume"].iloc[-1] > 1.5 * avg_vol

    return close > pivot_high and vol_expansion