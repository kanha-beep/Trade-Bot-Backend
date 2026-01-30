def detect_head_shoulders(df):
    recent = df.tail(60)

    highs = recent["High"]
    head = highs.idxmax()
    left = highs[:head].idxmax()
    right = highs[head:].idxmax()

    valid_shape = highs[head] > highs[left] and highs[head] > highs[right]

    neckline = recent["Low"].rolling(10).min().iloc[-1]

    breakdown = (
        df["Close"].iloc[-1] < neckline
        and df["Volume"].iloc[-1] > df["Volume"].rolling(20).mean().iloc[-1]
    )

    return valid_shape and breakdown
