def get_stop_loss(price, sl_pct=4):
    sl_price = price * (1 - sl_pct / 100)

    # if sell_signal:
    #     return "EXIT_NOW"

    return sl_price


def calculate_sl(price, sl_pct=None, sl_on_sell=False, sell_signal=False):
    """
    Returns stop-loss price

    sl_pct       → percentage SL (3–5)
    sl_on_sell   → enable SL on SELL crossover
    sell_signal  → SELL signal from strategy
    """

    # Percentage based SL (3–5%)
    if sl_pct is not None:
        return price * (1 - sl_pct / 100)

    # Indicator based SL (exit on SELL signal)
    if sl_on_sell and sell_signal:
        return "EXIT_NOW"

    return None
