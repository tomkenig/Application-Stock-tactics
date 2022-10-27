# todo v0.02: create view to quick view structured data
# todo v0.02: create def's
# DONE: todo: error handling with logs
# todo v0.02: add version avariable in json file??
# Stock tactics v0.02dev

from db_works import db_connect
import measures_and_dimensions as md
import json
import errhandler as eh

if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, \
    db_tactics_table_name, db_tactics_groups_table_name, \
    db_tactics_analyse_table_name, db_tactics_results_table_name, db_tactics_workers_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = \
        md.get_settings_json()
    cursor, cnxn = db_connect()

    tactic_group_data = {
        "tactic_group_name": "ROC first tests",
        "tactic_group_category": "single indicators",
        "tactic_group_stock_tactics_version": "v0.01",
        "download_settings_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "test_stake": [100],
        "buy_indicator_1_name": ["roc_6", "roc_7", "roc_9", "roc_10", "roc_12", "roc_14", "roc_16", "roc_20", "roc_21", "roc_24", "roc_30", "roc_50", "roc_100", "roc_200"],
        "buy_indicator_1_value": [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -12, -15],
        "buy_indicator_1_operator": ["<"],
        "buy_indicator_1_functions": "get_indicators_momentum_roc([6, 7, 9, 10, 12, 14, 16, 20, 21, 24, 25, 30, 50, 100, 200])",
        "yield_expected": [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.15, 0.17, 0.2, 0.25, 0.3, 0.35, 0.4],
        "wait_periods": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20],
        "standard_fee": [0.001]
    }

    print(json.dumps(tactic_group_data))
    try:
        cursor.execute(
            "INSERT INTO " + db_tactics_schema_name + "." + db_tactics_groups_table_name +
            " (tactic_group_name, tactic_group_category, "
            "tactic_group_status_id, tactic_group_data, buy_indicator_1_functions)  "
            "values (%s, %s, %s, %s, %s)", (tactic_group_data["tactic_group_name"],
                                            tactic_group_data["tactic_group_category"],
                                            0,
                                            json.dumps(tactic_group_data),
                                            str(tactic_group_data["buy_indicator_1_functions"])))  # function easy to use
        cnxn.commit()
        print("new row inserted, record id:" + str(cursor.lastrowid))
    except Exception as e:
        eh.errhandler_log(e)
