# todo: there are no need to be more than one representation of buy_indictator_functions in set and db
# todo: save numer of tactic group ID in tactics table also
# todo: correct tactic group id
# todo: correct buy_indicator_1_functions - take them from tactic_groups table
# todo: yield expectes as variable
# todo: md5 hash on json with variables
# todo: need to be equal as m&d names
# libs
from db_works import db_connect
import itertools
import measures_and_dimensions as md
import hashlib as hl


def get_tactics_category():
    cursor.execute("SELECT tactic_id, download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, "
                   "buy_indicator_1_operator, buy_indicator_1_functions, yield_expected, wait_periods "
                   "FROM " + db_tactics_schema_name + "." + db_tactics_groups_table_name + " "
                   " where tactic_group_status_id = 0 ;")
    tactics_group_data = cursor.fetchall()
    return tactics_group_data


# configs and connection

if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, db_tactics_groups_table_name \
        , db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = md.get_settings_json()
    cursor, cnxn = db_connect()

    download_settings_id = [3] # 2, 3] #, 4, 5] # , 6, 7, 10, 11]
    test_stake = [100]
    buy_indicator_1_name = ["roc_7", "roc_9", "roc_12", "roc_14"]
    buy_indicator_1_value = [-3, -4, -5, -6, -7, -8, -9, -10]
    buy_indicator_1_operator = ["<"]
    buy_indicator_1_functions = ["get_indicators_momentum_roc([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])"]
    yield_expected = [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.1]
    wait_periods = [8, 9, 10 , 11, 12, 13, 14, 15]


    # tactic group insert
    tactic_group_id = 1
    tactic_group_name = "RSI first tests"
    tactic_group_stock_tactics_version = '0.01'

    cursor.execute("SELECT tactic_group_id, tactic_group_name from " + db_tactics_schema_name + "." + db_tactics_groups_table_name + " WHERE tactic_group_status_id = 0;")


    # tactics insert
    x = []
    crosslists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, buy_indicator_1_operator, buy_indicator_1_functions, yield_expected, wait_periods ]
    for element in itertools.product(*crosslists):
        x.append(element)
        print(element)

    print(len(x))

    for y in x:
        cursor.execute("INSERT INTO " + db_tactics_schema_name + "." + db_tactics_table_name + " ( download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,buy_indicator_1_operator, "
                                              "buy_indicator_1_functions, yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_group_id)  values "
                                              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], 0.002, 0, 1))
        print(y)

    print("insert done")
    cnxn.commit()


    # saving vairables as tactic group
