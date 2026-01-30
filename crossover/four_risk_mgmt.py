ACCOUNT_BALANCE = 100000
RISK_PER_TRADE = 0.01


def risk_ok(price, sl):
    try:
        if price <= 0 or sl <= 0:
            return 0
        risk_amount = ACCOUNT_BALANCE * RISK_PER_TRADE
        price_diff = abs(price - sl)
        if price_diff == 0:
            return 0
        qty = risk_amount // price_diff
        return int(qty)
    except Exception as e:
        print(f"Risk calculation error: {e}")
        return 0
