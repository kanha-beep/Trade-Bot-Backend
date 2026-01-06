import yfinance as yf


def fetch_data(symbols, interval="1d", period="25y"):
    df = yf.download(
        symbols, interval=interval, period=period, group_by="ticker", progress=False
    )
    return df
