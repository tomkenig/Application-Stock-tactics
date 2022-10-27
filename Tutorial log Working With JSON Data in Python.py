import json


##
# json.loads() takes in a string and returns a json object.

# json.dumps() takes in a json object and returns a string.

tactic_group_data = {
    "tactic_group_name": "RSI first tests",
    "tactic_group_category": "single indicators",
    "tactic_group_stock_tactics_version": "0.01",
    "download_settings_id": [3],
    "test_stake": [100],
    "buy_indicator_1_name": ["roc_7", "roc_9", "roc_12", "roc_14"],
    "buy_indicator_1_value": [-3, -4, -5, -6, -7, -8, -9, -10],
    "buy_indicator_1_operator": ["<"],
    "buy_indicator_1_functions": ["get_indicators_momentum_roc([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])"],
    "yield_expected": [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.1],
    "wait_periods": [8, 9, 10, 11, 12, 13, 14, 15]
}

print(type(tactic_group_data))

print(tactic_group_data["tactic_group_name"])