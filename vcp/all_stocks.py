# import pandas as pd
# import requests
# from io import StringIO

# def get_all_nse_symbols():
#     url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

#     session = requests.Session()
#     session.headers.update({
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#         "Referer": "https://www.nseindia.com/",
#         "Accept": "text/csv,*/*",
#     })

#     # First hit NSE homepage to get cookies
#     session.get("https://www.nseindia.com", timeout=10)

#     # Now fetch CSV
#     r = session.get(url, timeout=10)
#     r.raise_for_status()

#     # Safety check
#     if "SYMBOL" not in r.text[:200]:
#         raise Exception("NSE blocked CSV (HTML received instead)")

#     df = pd.read_csv(StringIO(r.text))
#     symbols = df["SYMBOL"].dropna().unique()
#     # print("df:", df)
#     return [f"{s}.NS" for s in symbols]


# if __name__ == "__main__":
#     ALL_SYMBOLS = get_all_nse_symbols()
#     with open("all_symbols.py", "w") as f:
#         f.write("ALL_SYMBOLS = " + repr(ALL_SYMBOLS))
#     # print("Total stocks:", len(ALL_SYMBOLS))
#     # print("First 20:", ALL_SYMBOLS[:20])
