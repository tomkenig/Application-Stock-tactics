# libs
from db_works import db_connect
import itertools
import measures_and_dimensions as md
# tactics_categories
tactic_group_name = "RSI first tests"

# configs
db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, \
db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = md.get_settings_json()

cursor, cnxn = db_connect()


# tastics_for_tests RSI

# todo: need to be equal as m&d names
download_settings_id = [3] # 2, 3] #, 4, 5] # , 6, 7, 10, 11]
test_stake = [100]
buy_indicator_1_functions = ["get_indicators_momentum_roc([7, 9, 12, 14, 20, 21, 24, 25])"]
buy_indicator_1_name = ["roc_7", "roc_9", "roc_12", "roc_14"]
buy_indicator_1_value = [-3, -4, -5, -6, -7, -8, -9, -10]
buy_indicator_1_operator = ["<"]


# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [ 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.1]
wait_periods = [8, 9, 10 , 11, 12, 13, 14, 15] #, 16, 17, 18, 19, 20] #, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 25, 40, 45, 50, 60, 70, 80, 90, 100]

x = []
somelists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, buy_indicator_1_operator, yield_expected, wait_periods ]
for element in itertools.product(*somelists):
    x.append(element)
    print(element)

print(len(x))

for y in x:
    cursor.execute("INSERT INTO " + db_tactics_schema_name + "." + db_tactics_table_name + " ( download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,buy_indicator_1_operator, "
                                          "yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_group_id)  values "
                                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (y[0], y[1], y[2], y[3], y[4], y[5], y[6], 0.002, 0, 1))
    print(y)

print("insert done")
cnxn.commit()
