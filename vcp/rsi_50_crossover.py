def rsi_50_crossover(df):
    if len(df) < 2 or "RSI" not in df:
        return False
    prev = df["RSI"].iloc[-2]
    curr = df["RSI"].iloc[-1]
    return prev < 50 and curr > 50 and 48 <= curr <= 55