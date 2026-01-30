import yfinance as yf
import numpy as np

def safe(val, default=0):
    return val if val is not None else default
def get_fundamentals(symbol: str) -> dict:
    stock = yf.Ticker(symbol)
    try:
        info = stock.info
    except Exception:
        return {}
    # financials = stock.financials
    # cashflow = stock.cashflow

    # Growth
    eps_growth = safe(info.get("earningsGrowth"))
    revenue_growth = safe(info.get("revenueGrowth"))

    # Profitability
    roe = safe(info.get("returnOnEquity"))
    roce = safe(info.get("returnOnAssets"))  # proxy if ROCE not available

    # Financial strength
    debt_to_equity = safe(info.get("debtToEquity")) / 100
    interest_coverage = safe(info.get("interestCoverage"))
    # operating_cf = (
    #     cashflow.loc["Total Cash From Operating Activities"].iloc[0]
    #     if not cashflow.empty and "Total Cash From Operating Activities" in cashflow.index
    #     else 0
    # )

    # Ownership + size
    promoter_holding = safe(info.get("heldPercentInsiders"))
    market_cap = safe(info.get("marketCap"))

    return {
        "eps_growth": eps_growth,
        "revenue_growth": revenue_growth,
        "roe": roe,
        "roce": roce,
        "debt_to_equity": debt_to_equity,
        "interest_coverage": interest_coverage,
        # "operating_cf": operating_cf,
        "promoter_holding": promoter_holding,
        "market_cap": market_cap,
    }