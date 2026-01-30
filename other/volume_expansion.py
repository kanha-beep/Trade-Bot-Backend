def volume_expansion(df):
    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    return df["Volume"].iloc[-1] > 1.5 * avg_vol
