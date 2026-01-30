# from calculate_ema import calculate_ema
# def detect_vcp(df):
#     required_cols = {"High", "Low", "Close", "Volume", "ATR"}
#     if len(df) < 50 or not required_cols.issubset(df.columns):
#         return False
#     # ATR contraction (allow small noise)
#     atr_recent = df["ATR"].tail(10)
#     atr_contracting = atr_recent.mean() < df["ATR"].rolling(20).mean().iloc[-1]
#     # Price contraction
#     ranges = (df["High"] - df["Low"])
#     range_recent = ranges.tail(10).mean()
#     range_prev = ranges.tail(20).head(10).mean()
#     range_contracting = range_recent < range_prev
#     # Volume contraction
#     vol_recent = df["Volume"].tail(10).mean()
#     vol_prev = df["Volume"].tail(20).head(10).mean()
#     volume_contracting = vol_recent < vol_prev
#     return atr_contracting and range_contracting and volume_contracting

# def detect_vcp(df):
#     required = {"High", "Low", "Close", "Volume", "ATR"}
#     if len(df) < 60 or not required.issubset(df.columns):
#         return False

#     # ----- PRICE contraction (3 legs) -----
#     ranges = df["High"] - df["Low"]
#     r1 = ranges.tail(30).head(10).mean()   # oldest
#     r2 = ranges.tail(20).head(10).mean()
#     r3 = ranges.tail(10).mean()            # latest

#     price_contracting = r1 > r2 > r3

#     # ----- ATR contraction (3 legs) -----
#     atr = df["ATR"]
#     a1 = atr.tail(30).head(10).mean()
#     a2 = atr.tail(20).head(10).mean()
#     a3 = atr.tail(10).mean()

#     atr_contracting = a1 > a2 > a3

#     # ----- Volume contraction (3 legs) -----
#     vol = df["Volume"]
#     v1 = vol.tail(30).head(10).mean()
#     v2 = vol.tail(20).head(10).mean()
#     v3 = vol.tail(10).mean()

#     volume_contracting = v1 > v2 > v3

#     return price_contracting and atr_contracting and volume_contracting
# def detect_vcp(df):
#     required = {"High", "Low", "Volume", "ATR"}
#     if len(df) < 60 or not required.issubset(df.columns):
#         return False

#     # Price range contraction
#     ranges = df["High"] - df["Low"]
#     r1 = ranges.tail(30).head(10).mean()
#     r2 = ranges.tail(20).head(10).mean()
#     r3 = ranges.tail(10).mean()
#     price_contracting = r1 > r2 > r3

#     # ATR contraction
#     atr = df["ATR"]
#     a1 = atr.tail(30).head(10).mean()
#     a2 = atr.tail(20).head(10).mean()
#     a3 = atr.tail(10).mean()
#     atr_contracting = a1 > a2 > a3

#     # Volume contraction
#     vol = df["Volume"]
#     v1 = vol.tail(30).head(10).mean()
#     v2 = vol.tail(20).head(10).mean()
#     v3 = vol.tail(10).mean()
#     volume_contracting = v1 > v2 > v3

#     return price_contracting and atr_contracting and volume_contracting
import numpy as np

def detect_vcp(
    close,
    high,
    low,
    volume,
    lookback=50,
    min_contractions=3
):
    close = np.array(close[-lookback:])
    high = np.array(high[-lookback:])
    low = np.array(low[-lookback:])
    volume = np.array(volume[-lookback:])

    # price range per candle
    ranges = (high - low) / close

    # split into contraction legs
    chunks = np.array_split(ranges, min_contractions)
    avg_ranges = [np.mean(c) for c in chunks]

    # 1️⃣ volatility must contract step-by-step
    for i in range(1, len(avg_ranges)):
        if avg_ranges[i] >= avg_ranges[i - 1]:
            return False

    # 2️⃣ higher lows (no deep selloff)
    lows = np.array(low)
    swing_lows = lows[lows < np.roll(lows, 1)]
    if len(swing_lows) < 2:
        return False
    if swing_lows[-1] <= swing_lows[-2]:
        return False

    # 3️⃣ volume dries up into last contraction
    vol_chunks = np.array_split(volume, min_contractions)
    avg_vols = [np.mean(v) for v in vol_chunks]

    for i in range(1, len(avg_vols)):
        if avg_vols[i] > avg_vols[i - 1]:
            return False

    return True
