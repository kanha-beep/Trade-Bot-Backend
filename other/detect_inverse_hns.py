def detect_inverse_hns(df):
    recent = df.tail(60)

    lows = recent["Low"]
    head = lows.idxmin()
    left = lows[:head].idxmin()
    right = lows[head:].idxmin()

    valid_shape = lows[head] < lows[left] and lows[head] < lows[right]

    neckline = recent["High"].rolling(10).max().iloc[-1]

    breakout = (
        df["Close"].iloc[-1] > neckline
        and df["Volume"].iloc[-1] > 1.5 * df["Volume"].rolling(20).mean().iloc[-1]
    )

    return valid_shape and breakout
