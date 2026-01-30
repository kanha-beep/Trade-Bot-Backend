import yfinance as yf
from server.vcp.login import ALL_SYMBOLS

valid = []
for s in ALL_SYMBOLS:
    try:
        yf.Ticker(s).info
        valid.append(s)
    except:
        pass