from db_works import db_connect
import itertools
import measures_and_dimensions as md
import hashlib as hl
import json

# configs and connection

if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, db_tactics_groups_table_name \
        , db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = md.get_settings_json()
    cursor, cnxn = db_connect()

    x = {
        "tactic_group_id": [3],
        "tactic_name": "RSI first tests",
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

    print(json.dumps(x))




    download_settings_id = [3] # 2, 3] #, 4, 5] # , 6, 7, 10, 11]
    test_stake = [100]
    buy_indicator_1_name = ["roc_7", "roc_9", "roc_12", "roc_14"]
    buy_indicator_1_value = [-3, -4, -5, -6, -7, -8, -9, -10]
    buy_indicator_1_operator = ["<"]
    buy_indicator_1_functions = ["get_indicators_momentum_roc([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])"]
    yield_expected = [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.1]
    wait_periods = [8, 9, 10, 11, 12, 13, 14, 15]


    # tactic group insert
    tactic_group_id = 1
    tactic_group_name = "RSI first tests"
    tactic_group_stock_tactics_version = '0.01'

    insert_string_1 = to_json(buy_indicator_1_name)