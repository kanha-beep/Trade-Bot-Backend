import numpy as np
from vcp.detect_vcp import detect_vcp


def _deep_contraction(df, factor=0.5):
    atr_long = df["ATR"].rolling(60).mean().iloc[-1]
    atr_short = df["ATR"].rolling(10).mean().iloc[-1]
    return atr_short < atr_long * factor


def _pivot_tight(df, candles=7, pct=0.02):
    high = df["High"].tail(candles).max()
    low = df["Low"].tail(candles).min()
    return (high - low) / df["Close"].iloc[-1] < pct


def _volume_pocket(df):
    vol = df["Volume"]
    return (
        vol.iloc[-1] > vol.tail(20).mean() and vol.tail(5).mean() < vol.tail(30).mean()
    )


def _ema_squeeze(df):
    if not {"EMA_21", "EMA_50", "EMA_200"}.issubset(df.columns):
        return False
    return df["EMA_21"].iloc[-1] > df["EMA_50"].iloc[-1] > df["EMA_200"].iloc[-1]


def _higher_lows(df, lookback=60):
    lows = df["Low"].tail(lookback)
    return lows.iloc[-1] > lows.min()


def _range_contraction(df, windows=(40, 25, 15)):
    ranges = []
    for w in windows:
        r = (df["High"].tail(w).max() - df["Low"].tail(w).min()) / df["Close"].iloc[-1]
        ranges.append(r)
    return ranges[0] > ranges[1] > ranges[2]


def _atr_contraction(df, windows=(40, 20)):
    atr_long = df["ATR"].tail(windows[0]).mean()
    atr_short = df["ATR"].tail(windows[1]).mean()
    return atr_short < atr_long * 0.7


def _volume_dry(df, windows=(30, 10)):
    vol_long = df["Volume"].tail(windows[0]).mean()
    vol_short = df["Volume"].tail(windows[1]).mean()
    return vol_short < vol_long * 0.6


def _near_high(df, pct=0.15):
    high = df["High"].rolling(120).max().iloc[-1]
    close = df["Close"].iloc[-1]
    return close > high * (1 - pct)


# =========================
# VCP VARIANTS
# =========================


def classic_vcp(df):
    return (
        _higher_lows(df)
        and _range_contraction(df)
        and _atr_contraction(df)
        and _volume_dry(df)
    )


def tight_vcp(df):
    return _range_contraction(df, windows=(30, 20, 10)) and _volume_dry(
        df, windows=(20, 7)
    )


def long_base_vcp(df):
    return (
        _higher_lows(df, lookback=120)
        and _atr_contraction(df, windows=(60, 30))
        and _near_high(df)
    )


def early_vcp(df):
    return _higher_lows(df) and _volume_dry(df)


def aggressive_vcp(df):
    return _range_contraction(df) and _atr_contraction(df)


def power_vcp(df):
    return classic_vcp(df) and _deep_contraction(df) and _pivot_tight(df)


def breakout_ready_vcp(df):
    return tight_vcp(df) and _pivot_tight(df, candles=5, pct=0.015) and _volume_dry(df)


def institutional_vcp(df):
    return long_base_vcp(df) and _volume_pocket(df)

# closes = df["Close"].tolist()
# highs = df["High"].tolist()
# lows = df["Low"].tolist()
# volumes = df["Volume"].tolist()
# def legacy_vcp(df):
#     detect_vcp(close, high, low, volume)



# =========================
# MASTER DETECTOR
# =========================


def detect_vcp_all(df):
    signals = []

    if classic_vcp(df):
        signals.append("CLASSIC_VCP")

    if tight_vcp(df):
        signals.append("TIGHT_VCP")

    if long_base_vcp(df):
        signals.append("LONG_BASE_VCP")

    if early_vcp(df):
        signals.append("EARLY_VCP")

    if aggressive_vcp(df):
        signals.append("AGGRESSIVE_VCP")

    if power_vcp(df):
        signals.append("POWER_VCP")

    if breakout_ready_vcp(df):
        signals.append("BREAKOUT_READY_VCP")

    if institutional_vcp(df):
        signals.append("INSTITUTIONAL_VCP")

    # if legacy_vcp(df):
    #     signals.append("LEGACY_VCP")

    return signals
