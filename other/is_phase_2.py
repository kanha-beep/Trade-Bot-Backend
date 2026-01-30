def is_phase_2(df):
    return (
        df["EMA_50"].iloc[-1] > df["EMA_200"].iloc[-1]
        and df["Close"].iloc[-1] > df["EMA_50"].iloc[-1]
        and df["EMA_200"].iloc[-1] > df["EMA_200"].iloc[-5]
    )
