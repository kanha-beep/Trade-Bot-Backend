def detect_cup_handle(df):
    recent = df.tail(60)

    left_high = recent["High"][:20].max()
    right_high = recent["High"][-20:].max()
    cup_depth = recent["Low"].min()

    cup_valid = abs(left_high - right_high) / left_high < 0.05
    rounded_bottom = cup_depth < left_high * 0.9

    handle = recent.tail(10)
    handle_depth = handle["Low"].min()
    handle_valid = handle_depth > cup_depth

    vol_cup = recent["Volume"][:30].mean()
    vol_handle = handle["Volume"].mean()
    volume_dry = vol_handle < vol_cup * 0.7

    breakout = (
        df["Close"].iloc[-1] > right_high
        and df["Volume"].iloc[-1] > 1.5 * df["Volume"].rolling(20).mean().iloc[-1]
    )

    return cup_valid and rounded_bottom and handle_valid and volume_dry and breakout
