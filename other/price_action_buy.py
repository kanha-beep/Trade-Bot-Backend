def price_action_buy(df):
    return detect_cup_handle(df) or detect_inverse_hns(df) or upward_channel(df)


if detect_head_shoulders(df) or downward_channel(df):
    skip_trade = True
