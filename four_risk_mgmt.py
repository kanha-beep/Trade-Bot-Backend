ACCOUNT_BALANCE = 100000
RISK_PER_TRADE = 0.01


def risk_ok(price, sl):
    risk_amount = ACCOUNT_BALANCE * RISK_PER_TRADE
    qty = risk_amount // abs(price - sl)
    return int(qty)
