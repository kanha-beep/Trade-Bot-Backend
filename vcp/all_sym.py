import pandas as pd
import yfinance as yf
import requests
from io import StringIO


# 1. Fetch NSE equity master CSV
def get_nse_yfinance_symbols(validate=True, period="5d"):
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    csv_text = requests.get(url, headers=headers).text
    df = pd.read_csv(StringIO(csv_text))

    # 2. Keep only main equity series
    df = df[df[" SERIES"] == "EQ"]

    # 3. Convert to yfinance tickers
    df["YF_SYMBOL"] = df["SYMBOL"].str.strip() + ".NS"
    symbols = df["YF_SYMBOL"].tolist()

    print("Total NSE EQ symbols:", len(symbols))
    print(symbols[:10])
    if not validate:
        return symbols  # ← THIS was missing
    valid = []
    for s in symbols:
        try:
            d = yf.Ticker(s).history(period="5d")
            if not d.empty:
                valid.append(s)
        except:
            pass
    return valid


# all_symbols = get_nse_yfinance_symbols(validate=False)
# print(len(all_symbols))  # ✅ prints count
# print(all_symbols[:10])
