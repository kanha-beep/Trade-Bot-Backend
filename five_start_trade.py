# state = {"in_trade": False, "cooldown_until": None}
state = {}


def can_trade(symbol):
    return not state.get(symbol, False)
