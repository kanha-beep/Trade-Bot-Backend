def position_size(capital, entry, stop, risk_pct=0.01):
    risk_amount = capital * risk_pct
    per_share_risk = entry - stop

    if per_share_risk <= 0:
        return 0

    return int(risk_amount // per_share_risk)
