def fundamentals_pass(f: dict) -> bool:
    if not f:
        return False

    required = [
        f.get("eps_growth"),
        # f.get("revenue_growth"),
        # f.get("roe"),
        f.get("roce"),
        f.get("market_cap"),
    ]

    if any(v is None for v in required):
        return False

    return (
        f["eps_growth"] >= 0.20
        # and f["revenue_growth"] >= 0.15
        # and f["roe"] >= 0.15
        and f["roce"] >= 0.18
        # and f["debt_to_equity"] <= 0.5
        # and (f["interest_coverage"] or 0) >= 5
        # and (f["operating_cf"] or 0) > 0
        # and (f["promoter_holding"] or 0) >= 0.40
        and 1_000_000_000 <= f["market_cap"] <= 20_000_000_000_000
    )