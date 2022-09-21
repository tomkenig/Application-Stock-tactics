# libs
from db_works import db_connect
import itertools
import measures_and_dimensions as md
# tactics_categories
tactic_group_name = "RSI first tests"

# configs
db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, \
db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH = md.get_settings_json()

cursor, cnxn = db_connect()


# tastics_for_tests RSI


download_settings_id = [11] # 2, 3] #, 4, 5] # , 6, 7, 10, 11]
test_stake = [100]
buy_indicator_1_functions = ["get_indicators_momentum_rsi([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])"]
buy_indicator_1_name = ["rsi_6"] # , "rsi_10", "rsi_12", "rsi_14"] #, "rsi_20", "rsi_24"] # todo: need to be equal as m&d names
buy_indicator_1_value = [0.05, 0.1, 0.15, 0.20, 0.25] # , 0.30, 0.35, 0.40, 0.45, 0.50]
buy_indicator_1_operator = ["<"]


# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [0.003, 0.004, 0.005] # , 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016,
                 # 0.017, 0.018, 0.019, 0.02, 0.025, 0.03] #, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5]
wait_periods = [3, 4, 5, 6, 7, 8, 9] #, 10 , 11, 12, 13, 14, 15] #, 16, 17, 18, 19, 20] #, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 25, 40, 45, 50, 60, 70, 80, 90, 100]

x = []
somelists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, buy_indicator_1_operator, yield_expected, wait_periods ]
for element in itertools.product(*somelists):
    x.append(element)
    # print(element)

for y in x:
    cursor.execute("INSERT INTO " + db_tactics_schema_name + "." + db_tactics_table_name + " ( download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,buy_indicator_1_operator, "
                                          "yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_group_id)  values "
                                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (y[0], y[1], y[2], y[3], y[4], y[5], y[6], 0.002, 0, 1))

print("insert done")
cnxn.commit()
