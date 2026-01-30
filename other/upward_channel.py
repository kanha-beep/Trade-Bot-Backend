def upward_channel(df):
    highs = df["High"].tail(30)
    lows = df["Low"].tail(30)

    return highs.iloc[-1] > highs.iloc[0] and lows.iloc[-1] > lows.iloc[0]
