def volume_dryness(df):
     if len(df) < 20 or "Volume" not in df:
         return False
     avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
     curr_vol = df["Volume"].iloc[-1]
     return curr_vol < 0.7 * avg_vol
    # return df["Volume"].iloc[-1] < 0.7 * avg_vol