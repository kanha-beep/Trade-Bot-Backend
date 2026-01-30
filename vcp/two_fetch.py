import yfinance as yf
import warnings

def fetch_data(symbols, period="3y", interval="1d"):
    # Suppress yfinance warnings about delisted stocks
    warnings.filterwarnings("ignore", message=".*possibly delisted.*")
    
    df = yf.download(
        symbols,
        period=period,
        interval=interval,
        group_by="ticker",
        progress=False,
        threads=True,
        auto_adjust=False,
    )
    return df
# yf.download(
#     tickers=batch,
#     period="2y",
#     interval="1d",
#     group_by="ticker",
#     auto_adjust=True,
#     threads=False,
#     progress=False
# )
