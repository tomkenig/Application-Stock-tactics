# Stock tactics v0.02dev
# DONE: todo: v0.01: simple error handling with logs
# DONE: todo: v0.02: create view to quick view structured data
# todo v0.02: create def's
# todo v0.02: add version number to json file??
# todo v0.02: Documentation: list indicators names and tech names - easier to group test.

from db_works import db_connect
import measures_and_dimensions as md
import json
import errhandler as eh

if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, \
    db_tactics_table_name, db_tactics_groups_table_name, \
    db_tactics_analyse_table_name, db_tactics_results_table_name, db_tactics_workers_table_name, db_tactics_config_table_name, TMP_DIR_PATH, \
    TACTICS_PACK_SIZE, worker_tactics_generator_work_hours, worker_tactics_generator_sleep = \
        md.get_settings_json()
    cursor, cnxn = db_connect()

    tactic_group_data = {
        "tactic_group_name": "AVG_CROSS first tests 20221119",
        "tactic_group_category": "single indicators",
        "tactic_group_stock_tactics_version": "0.02dev",
        "download_settings_id": [3],  #2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "test_stake": [100],
        "buy_indicator_1_name": ["cross_sma_50_200", "cross_sma_7_14", "cross_sma_7_21", "cross_sma_7_50",
                                 "cross_sma_price_7", "cross_sma_price_14", "cross_sma_price_21",
                                 "cross_sma_price_50", "cross_sma_price_200"],
        "buy_indicator_1_value": [1],
        "buy_indicator_1_operator": ["=="],
        "buy_indicator_1_functions": "get_indicators_averages([7, 14, 21, 50, 200]), get_indicators_averages_cross()",
        "yield_expected": [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.15, 0.17, 0.2, 0.25, 0.3, 0.35, 0.4],
        "wait_periods": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
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
