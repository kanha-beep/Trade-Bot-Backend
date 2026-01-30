# from calculate_ema import calculate_ema
# def above_200ema(df, days=45):
#     if len(df) < max(200, days) or "Close" not in df:
#         return False
#     df = df.copy()  # avoid SettingWithCopyWarning
#     df["EMA_200"] = calculate_ema(df["Close"], 200)
#     recent_df = df.tail(days)
#     # Check: Close > EMA200 for ALL last N days
#     condition = (recent_df["Close"] > recent_df["EMA_200"]).all()
#     # print(f"Above 200 EMA for last {days} days: {condition}")
#     return condition

from vcp.calculate_ema import calculate_ema

def above_200ema(df, days=45):
    if len(df) < max(200, days) or "Close" not in df:
        return False
    ema_200 = calculate_ema(df["Close"], 200)
    recent_close = df["Close"].tail(days)
    recent_ema = ema_200.tail(days)
    return (recent_close > recent_ema).all()