# todo: v0.02: combination table. Can be stored in other schema
# todo: v0.02: pep8
# todo: v0.02: do smth with updates fe.: one update DB/INE INSERT. Less connections to DB
# todo: v0.02: separate tactics and OHLC (can be even on other dbs)
# todo: v0.02: fix to many print
# todo: v0.02: code clean
# todo: v0.02: fix zero-devide error in data frame (hard to reach)
# todo: v0.02: create process to delete old results and tactics
# todo: v0.02: decide witch results are valuable. Fe: every year winn, almost all months win, minimum profit etc.
# todo: v0.02: add to results string 4 additional values with times, with open and close times. It will be helpfull in
#  multitactic analysis. Which are the best and doesn't cross other tactics
# todo: v0.02: "if score_2 >= 200:" -- add this int config json
# todo: v0.02: indicators: RSI divergention price vs RSI
# todo: v0.02: indicators: all williams indicators
# DONE: todo: update and lock records
# DONE: todo: tactic_status table with data
# DONE: todo: insert tactic generator pre data in db
# DONE: todo: do smth with long sting in tactics (anl. functions string). f. string in tactic generator
# DONE: todo: Ad Worker id \
# DONE: todo: test_stock_fee = -0.002, do dynamic not static!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOW
# DONE: todo: error handling
# DONE: todo: # Delete it on prod open_time = str(1631042226) + '000'
# DONE: todo: test parallel workers
# todo: v0.02: functions interpretation
# todo: v0.02: anl functions check
# todo: v0.02: documentation
# todo: v0.02: test tactic signal creation (ok/not)
# DONE: todo: change 0.01dev to 0.01 and add tag into all files
# DONE: todo: v0.02: fix errors, when more than one tactic_Group is in one set to analayse
# DONE: todo: v0.02: tactic_workers change - always insert new record (new worker)
# todo: v0.02: indicators outside TA-LIB (fe. CHOP, other from trafing course FXMAG (aligators etc.)
# todo: v0.02: bulk update status tactics to check - in one query
"""
pip install mysql-connector-python
pip install pandas
pip install numpy
plan 2022/02/03
"""
# Stock tactics v0.02dev

# libs
# import datetime
from db_works import db_connect
import pandas as pd
import numpy as np
import pandas_ta as pta  # https://mrjbq7.github.io/ta-lib/
# import talib as ta  # install from whl file < https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import json
import time
import os
import errhandler as eh
import uuid  # https://docs.python.org/3/library/uuid.html
import openpyxl
import socket

# todo: make better. All from json
# get settings from config json
def get_settings_json():
    with open("global_config.json") as json_conf:
        app_conf = (json.load(json_conf))
    print("conf file opened")
    db_klines_schema_name = app_conf["db_klines_schema_name"]
    db_tactics_schema_name = app_conf["db_tactics_schema_name"]
    db_klines_anl_table_name = app_conf["db_klines_anl_table_name"]
    db_binance_settings_table_name = app_conf["db_binance_settings_table_name"]
    db_tactics_table_name = app_conf["db_tactics_table_name"]
    db_tactics_groups_table_name = app_conf["db_tactics_groups_table_name"]
    db_tactics_analyse_table_name = app_conf["db_tactics_analyse_table_name"]
    db_tactics_results_table_name = app_conf["db_tactics_results_table_name"]
    db_tactics_workers_table_name = app_conf["db_tactics_workers_table_name"]
    db_tactics_config_table_name = app_conf["db_tactics_config_table_name"]
    TMP_DIR_PATH = app_conf["tmp_dir_path"]
    TACTICS_PACK_SIZE = app_conf["tactics_pack_size"]
    worker_tactics_generator_work_hours = app_conf["worker_tactics_generator_work_hours"]
    worker_tactics_generator_sleep = app_conf["worker_tactics_generator_sleep"]

    return db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, \
           db_tactics_table_name, db_tactics_groups_table_name, db_tactics_analyse_table_name, \
           db_tactics_results_table_name, db_tactics_workers_table_name, db_tactics_config_table_name, \
           TMP_DIR_PATH, TACTICS_PACK_SIZE, \
           worker_tactics_generator_work_hours, worker_tactics_generator_sleep


# create temporary directory for downloaded files
def create_temp_dir(tmp_dir_path_in):
    try:
        os.mkdir(tmp_dir_path_in)
    except OSError as error:
        print(error)

# delete old files if exist in temp directory
def delete_old_files():
    try:
        for f in os.listdir(TMP_DIR_PATH[0:len(TMP_DIR_PATH)-1]):
            os.remove(os.path.join(TMP_DIR_PATH[0:len(TMP_DIR_PATH)-1], f))
        print("old files deleted")
    except OSError as error:
        print(error)

# todo:
def lock_other_workers():
    print("locking...")
    cursor.execute("LOCK TABLES " + db_tactics_schema_name + "." + db_tactics_table_name + " WRITE"
                   # ", " + db_tactics_schema_name + "." + db_tactics_groups_table_name + " WRITE"
                   # ", " + db_tactics_schema_name + "." + db_binance_settings_table_name + " WRITE"                                                                               
                   ", " + db_tactics_schema_name + "." + db_tactics_analyse_table_name + " READ;")
    print("locking done")

def unlock_other_workers():
    print("unlocking...")
    cursor.execute("UNLOCK TABLES;")
    print("unlocking done")

def register_worker():
    worker_hostname = str(socket.gethostname())
    worker_ipaddress = str(socket.gethostbyname(socket.gethostname()))
    print(worker_hostname)
    try:
        try:
            cursor.execute("INSERT into " + db_tactics_schema_name + "." + db_tactics_workers_table_name + " (worker_hostname, worker_ipaddress) values ('"+worker_hostname+"', '"+worker_ipaddress+"') ; ")
            worker_id = str(cursor.lastrowid)
            print(worker_id)
            cnxn.commit()
        except:
            exit()
    except Exception as e:
        eh.errhandler_log(e)
    return worker_hostname, worker_id


# todo: lock record status in get_tactics_to_check()
def get_tactics_to_check():
    lock_other_workers()
    try:
        cursor.execute("SELECT tactic_id, a.download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, "
                       "buy_indicator_1_operator, buy_indicator_1_functions, yield_expected, wait_periods, stock_fee "
                       "FROM " + db_tactics_schema_name + "." + db_tactics_analyse_table_name + " a "
                       " join (SELECT download_settings_id, tactic_group_id FROM " + db_tactics_schema_name + "." + db_tactics_table_name +
                       " where tactic_status_id = 0 limit 1 ) b "
                       " on a.download_settings_id = b.download_settings_id "
                       " and a.tactic_group_id = b.tactic_group_id"                                                                         
                       " where tactic_status_id = 0 limit " + str(TACTICS_PACK_SIZE) + ";")
        tactics_data = cursor.fetchall()
        update_tactics_data = tactics_data.copy()
    except Exception as e:
        eh.errhandler_log(e)

    # change records status
    for i in update_tactics_data:
        print(i[0])
        cursor.execute(
            "UPDATE " + db_tactics_schema_name + "." + db_tactics_table_name +" SET tactic_status_id = 1, worker_id = " + str(worker_id) + " where tactic_id = " + str(
                i[0]) + " ")
    print("update status done")
    unlock_other_workers()
    cnxn.commit()
    return tactics_data

# download OHLC data from DWH
def get_ohlc_data():
    cursor.execute("SELECT * FROM " + db_klines_schema_name + "." + db_klines_anl_table_name + " where "
                                     "download_settings_id = '" + str(download_settings_id) + "' ")
    df = pd.DataFrame(cursor.fetchall())
    df_bak = df.copy()  # absolutly needed. Simple assignment doesn't work
    print("OHLC data ready")
    return df, df_bak


def get_structured_data():
    df.columns = ["open_time",
                  "open",
                  "high",
                  "low",
                  "close",
                  "volume",
                  "close_time",
                  "quote_asset_volume",
                  "number_of_trades",
                  "taker_buy_base_asset_volume",
                  "taker_buy_quote_asset_volume",
                  "ignore",
                  "market",
                  "tick_interval",
                  "data_granulation",
                  "stock_type",
                  "stock_exchange",
                  "download_settings_id",
                  "insert_timestamp",
                  "open_datetime",
                  "close_datetime"]


def get_indicators_basics():
    # verified
    # basics
    df["open_time_dt"] = pd.to_datetime(df["open_datetime"], unit='ms')
    df["open_time_yr"] = df["open_time_dt"].dt.year
    df["open_time_mnt"] = df["open_time_dt"].dt.month
    df["open_time_dy"] = df["open_time_dt"].dt.day

    df["change_val"] = df.close - df.open
    df["change_perc"] = df.close / df.open - 1
    df["amplitude_val"] = df.high - df.low
    df["amplitude_perc"] = df.high - df.low / df.open
    df["up_down"] = np.where(df["close"] - df["close"].shift(1) > 0, 1, -1)  # 1up / -1 down


def get_indicators_trend_and_changes():
    # NOT verified: it's trend change indicator/breakpoint indicator?
    # token: trend up/down 1 / -1
    # definition: in custom period sums of change are up or down.
    # you an combine it with ADX - trend strength by multiply both ie. -1 * 40
    # 1 - up-trend in x periods -1 - down-trend in x periods
    # values -1 (negative), 1 (positive)
    df["token_change_7"] = df["change_val"].rolling(7).sum()
    df["token_trend_7"] = np.where(df["token_change_7"] > 0, 1, -1)
    df["token_change_10"] = df["change_val"].rolling(10).sum()
    df["token_trend_10"] = np.where(df["token_change_10"] > 0, 1, -1)
    df["token_change_14"] = df["change_val"].rolling(14).sum() # oryginal
    df["token_trend_14"] = np.where(df["token_change_14"] > 0, 1, -1)
    df["token_change_24"] = df["change_val"].rolling(24).sum()
    df["token_trend_24"] = np.where(df["token_change_24"] > 0, 1, -1)
    df["token_change_50"] = df["change_val"].rolling(50).sum()
    df["token_trend_50"] = np.where(df["token_change_50"] > 0, 1, -1)
    df["token_change_100"] = df["change_val"].rolling(100).sum()
    df["token_trend_100"] = np.where(df["token_change_100"] > 0, 1, -1)
    df["token_change_200"] = df["change_val"].rolling(200).sum()
    df["token_trend_200"] = np.where(df["token_change_200"] > 0, 1, -1)

# AVERAGES
def get_indicators_averages(period_list):
    # verified tradingView
    # interpretation: not needed
    # SMA (Simple), WMA, EMA (Exponential)
    for i in period_list:
        df["sma_"+str(i)] = pta.sma(df["close"], length=i)
        df["wma_"+str(i)] = pta.wma(df["close"], length=i)
        df["ema_"+str(i)] = pta.ema(df["close"], length=i)

def get_indicators_averages_cross():
    # verified TradingView
    # GAME PROPOSAL: -1 - continue downtrend ; +1 - continue uptrend
    # fe: Buy when +1
    # Moving average crossing moving average
    # golden cross (1) and death cross (-1)
    df["cross_sma_50_200"] = np.where((df["sma_50"] - df["sma_200"] < 0) & (df["sma_50"].shift(1)
                                                                            - df["sma_200"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_50"] - df["sma_200"] > 0) & (df["sma_50"].shift(1)
                                                                            - df["sma_200"].shift(1) < 0), 1, 0)
    df["cross_sma_7_14"] = np.where((df["sma_7"] - df["sma_14"] < 0) & (df["sma_7"].shift(1)
                                                                        - df["sma_14"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_14"] > 0) & (df["sma_7"].shift(1)
                                                                          - df["sma_14"].shift(1) < 0), 1, 0)
    df["cross_sma_7_21"] = np.where((df["sma_7"] - df["sma_21"] < 0) & (df["sma_7"].shift(1)
                                                                        - df["sma_21"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_21"] > 0) & (df["sma_7"].shift(1)
                                                                          - df["sma_21"].shift(1) < 0), 1, 0)
    df["cross_sma_7_50"] = np.where((df["sma_7"] - df["sma_50"] < 0) & (df["sma_7"].shift(1)
                                                                        - df["sma_50"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_50"] > 0) & (df["sma_7"].shift(1)
                                                                          - df["sma_50"].shift(1) < 0), 1, 0)

    # moving average crossing price 7, 14, 21, 50
    df["cross_sma_price_7"] = np.where((df["sma_7"] - df["close"] < 0) & (df["sma_7"].shift(1) - df["close"].shift(1) > 0), 1, 0) +\
                             np.where((df["sma_7"] - df["close"] > 0) & (df["sma_7"].shift(1) - df["close"].shift(1) < 0), -1, 0)
    df["cross_sma_price_14"] = np.where((df["sma_14"] - df["close"] < 0) & (df["sma_14"].shift(1) - df["close"].shift(1) > 0), 1, 0) +\
                             np.where((df["sma_14"] - df["close"] > 0) & (df["sma_14"].shift(1) - df["close"].shift(1) < 0), -1, 0)
    df["cross_sma_price_21"] = np.where((df["sma_21"] - df["close"] < 0) & (df["sma_21"].shift(1) - df["close"].shift(1) > 0), 1, 0) +\
                             np.where((df["sma_21"] - df["close"] > 0) & (df["sma_21"].shift(1) - df["close"].shift(1) < 0), -1, 0)
    # cross_sma_price_50 seems to be a good indicator in 2020 and 2021 in daily intervals. Better than 7,14,21
    df["cross_sma_price_50"] = np.where((df["sma_50"] - df["close"] < 0) & (df["sma_50"].shift(1) - df["close"].shift(1) > 0), 1, 0) +\
                             np.where((df["sma_50"] - df["close"] > 0) & (df["sma_50"].shift(1) - df["close"].shift(1) < 0), -1, 0)
    df["cross_sma_price_200"] = np.where((df["sma_200"] - df["close"] < 0) & (df["sma_200"].shift(1) - df["close"].shift(1) > 0), 1, 0) +\
                             np.where((df["sma_200"] - df["close"] > 0) & (df["sma_200"].shift(1) - df["close"].shift(1) < 0), -1, 0)

def get_indicators_averages_cross_periods():
    # todo: as def get_indicators_averages_cross(), but without 0 value. Show, where x is below y or under
    # 1-golden period ;-1 - death period
    df["cross_period_sma_50_200"] = np.where((df["sma_50"] < df["sma_200"]), -1, 1)
    df["cross_period_sma_7_14"] = np.where((df["sma_7"] < df["sma_14"]), -1, 1)
    df["cross_period_sma_7_21"] = np.where((df["sma_7"] < df["sma_21"]), -1, 1)
    df["cross_period_sma_7_50"] = np.where((df["sma_7"] < df["sma_50"]), -1, 1)

    # moving average crossing price 7, 14, 21, 50
    df["cross_period_sma_price_7"] = np.where((df["sma_7"] < df["close"]), -1, 1)
    df["cross_period_sma_price_14"] = np.where((df["sma_14"] < df["close"]), -1, 1)
    df["cross_period_sma_price_21"] = np.where((df["sma_21"] < df["close"]), -1, 1)
    df["cross_period_sma_price_50"] = np.where((df["sma_50"] < df["close"]), -1, 1)
    df["cross_period_sma_price_200"] = np.where((df["sma_200"] < df["close"]), -1, 1)


def get_indicators_momentum_roc(period_list):
    # ROC - Rate of change : ((price/prevPrice)-1)*100
    for i in period_list:
        df["roc_"+str(i)] = pta.roc(df["close"], length=i)

def get_indicators_momentum_rsi(period_list):
    # RSI - Relative Strength Index
    for i in period_list:
        df["rsi_"+str(i)] = pta.rsi(df["close"], length=i)


# PRINT RESULTS
def print_results():
    print(df)

# EXPORT TO EXCEL
def export_results_to_xls():
    df.to_excel("exports/export_settings" + str(download_settings_id) + "_" + str(time.time()) + ".xlsx")

# DO TESTS
def get_test_result(test_stake_in, test_indicator_buy_1_in, test_indicator_buy_value_1_in, buy_indicator_1_operator_in, test_yield_expect_in, test_wait_periods_in, stock_fee_in):
    test_stake = int(test_stake_in)
    test_indicator_buy_1 = test_indicator_buy_1_in
    test_indicator_buy_value_1 = test_indicator_buy_value_1_in
    test_yield_expect = test_yield_expect_in  # ie. 0.01=1%
    test_wait_periods = test_wait_periods_in  # ie. try to sell in next 6 periods (or 10)
    test_stoploss = -0.05  # must be minus
    test_stock_fee = -(stock_fee_in)  # must be minus

    #signal and operator from exec
    exec('df["tst_is_buy_signal"] = np.where((df[test_indicator_buy_1] '+ buy_indicator_1_operator_in +' test_indicator_buy_value_1), 1, 0)')
                                       #                                   & (df[test_indicator_buy_2] < test_indicator_buy_value_2)
                                       #                                   & (df[test_indicator_buy_3] < test_indicator_buy_value_3)
                                       #                                   & (df[test_indicator_buy_4] > test_indicator_buy_value_4)
                                       #, 1, 0)


    df["tst_sell_price"] = df["close"] * test_yield_expect + df["close"]
    df["tst_sell_stoploss_price"] = df["close"] + df["close"] * test_stoploss # must be plus
    df["tst_high_in_sell_period"] = df["high"].rolling(test_wait_periods).max().shift(-test_wait_periods)
    df["tst_low_in_sell_period"] = df["low"].rolling(test_wait_periods).min().shift(-test_wait_periods)
    df["tst_sell_after_yield"] = np.where(df['tst_high_in_sell_period'] >= df["tst_sell_price"], 1, 0)
    df["tst_sell_after_stoploss"] = np.where(df['tst_low_in_sell_period'] <= df["tst_sell_stoploss_price"], 1, 0)
    df["tst_sold_price"] = np.where(df['tst_sell_after_yield'] == 1, df["tst_sell_price"], df["close"].shift(-1 * test_wait_periods)) # market after time
    df["tst_sold_diff_perc"] = df["tst_sold_price"] / df["close"]
    df["tst_single_game_result"] = np.where(df['tst_sold_diff_perc'] > 1, 1, -1)
    df["tst_buy_sell_fee"] = test_stake * test_stock_fee  # todo: change later, but accuracy is good
    df["tst_single_game_earn"] = test_stake * df["tst_sold_diff_perc"] - test_stake
    df["tst_single_game_earn_minus_fees"] = (test_stake * df["tst_sold_diff_perc"] - test_stake) + df["tst_buy_sell_fee"]
    df["tst_single_game_earn_minus_fees_plus"] = np.where(df["tst_single_game_earn_minus_fees"] > 0, df["tst_single_game_earn_minus_fees"], None)
    df["tst_single_game_earn_minus_fees_minus"] = np.where(df["tst_single_game_earn_minus_fees"] < 0, df["tst_single_game_earn_minus_fees"], None)
    df["tst_single_game_earn_minus_fees_plus_sign"] = np.where(df["tst_single_game_earn_minus_fees"] > 0, 1, None)
    df["tst_single_game_earn_minus_fees_minus_sign"] = np.where(df["tst_single_game_earn_minus_fees"] < 0, -1, None)
    # todo: single game result with stoploss. Need improvement
    df["tst_single_game_earn_minus_fees_with_stoploss"] = np.where(df['tst_sell_after_stoploss'] == 1, test_stake * test_stoploss + df["tst_buy_sell_fee"], df["tst_single_game_earn_minus_fees"])


    # test_name = "tst_" & market & "_" & tick_interval & "_" & test_indicator_buy_1

    # print(df.info(verbose=True))

    # last check
    #print(df)

    # df2 aggr
    df2 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr", "open_time_mnt"]).\
        aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum",
                   "tst_single_game_earn_minus_fees_plus": "sum",
                   "tst_single_game_earn_minus_fees_minus": "sum",
                   "tst_single_game_earn_minus_fees_plus_sign": "sum",
                   "tst_single_game_earn_minus_fees_minus_sign": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })
    df2['earn_sign'] = np.sign(df2["tst_single_game_earn_minus_fees"])
    # print(df2)


    df3 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr"]).\
        aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum",
                   "tst_single_game_earn_minus_fees_plus": "sum",
                   "tst_single_game_earn_minus_fees_minus": "sum",
                   "tst_single_game_earn_minus_fees_plus_sign": "sum",
                   "tst_single_game_earn_minus_fees_minus_sign": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })
    df3['earn_sign'] = np.sign(df3["tst_single_game_earn_minus_fees"])
    # print(df3)

    # statistics

    df4 = df[df["tst_is_buy_signal"] == 1].aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum",
                   "tst_single_game_earn_minus_fees_plus": "sum",
                   "tst_single_game_earn_minus_fees_minus": "sum",
                   "tst_single_game_earn_minus_fees_plus_sign": "sum",
                   "tst_single_game_earn_minus_fees_minus_sign": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })
    # print(df4)

    # jsons with results
    result_string_1 = pd.DataFrame.to_json(df2)
    result_string_2 = pd.DataFrame.to_json(df3)
    result_string_3 = pd.DataFrame.to_json(df4)
    score_1 = df4["tst_is_buy_signal"]  # sum of buy signals:  -1 or 1
    score_2 = df4["tst_single_game_earn_minus_fees"]  # single game earn minus fees sum
    score_3 = df2["earn_sign"].sum() / df2["earn_sign"].count() if df2["earn_sign"].count() > 0 else 0  # monthly game earn percent
    score_4 = df3["earn_sign"].sum() / df3["earn_sign"].count() if df3["earn_sign"].count() > 0 else 0  # yearly game earn percent

    return result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4


if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, db_tactics_groups_table_name \
        , db_tactics_analyse_table_name, db_tactics_results_table_name, db_tactics_workers_table_name, db_tactics_config_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE, worker_tactics_generator_work_hours, worker_tactics_generator_sleep = get_settings_json()

    # create or clear temp dir
    create_temp_dir(TMP_DIR_PATH)

    # connect to db
    cursor, cnxn = db_connect()



    # register worker
    worker_hostname, worker_id = register_worker()

    # downloads tactics to check
    tactics_data = get_tactics_to_check()

    # get only data for one settings_id. Don't blend settings _id in one iteration
    download_settings_id = tactics_data[0][1]

    # print(tactics_data)
    print("select done settings done")

    # get OHLC data and create data frames
    df, df_bak = get_ohlc_data()
    # print(df)

    # create structure on tactics data
    get_structured_data()
    # print(df)

    # INDICATORS
    get_indicators_basics()

    # activate analytic functions from tactics set
    eval(tactics_data[0][6])
    print(tactics_data[0][6])

    # export results to xlsx. Work fine, when all analytical functions needed are activated.
    # export_results_to_xls()

    # print current df
    # print_results()

    # REAL TEST RUN
    print("begin test")
    print(len(tactics_data))

    df_bak = df.copy()

    for i in range(len(tactics_data)):  # in tactics_data:
        print(i)
        result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4 = get_test_result(
            int(tactics_data[i][2]), tactics_data[i][3], tactics_data[i][4], tactics_data[i][5], tactics_data[i][7],
            tactics_data[i][8], tactics_data[i][9])

        cursor.execute(
            "UPDATE " + db_tactics_schema_name + "." + db_tactics_table_name +" SET tactic_status_id = 2 where tactic_id = " + str(
                tactics_data[i][0]) + " ")
        print("update status done")
        cnxn.commit()

        # insert results if results are good enough
        # todo: read upper scripts and rewrite script listed below from 0
        print("score2:")
        print(score_2)

        if score_2 >= -1000000:  # 400 and score_1 >= 100 and score_4 == 1:  # and score_3 >= 0.75:
            cursor.execute(
                "INSERT INTO " + db_tactics_schema_name + "." + db_tactics_results_table_name +" (download_settings_id, tactic_id, result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4, worker_id)  values "
                                                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    download_settings_id, str(tactics_data[i][0]), result_string_1, result_string_2, result_string_3,
                    str(int(score_1)), str(int(score_2)), str(score_3), str(score_4), worker_id))

        print("insert done or not")
        df = df_bak.copy()  # absolutly needed. Simple assignment doesn't work in pandas
        # print(df)
        cnxn.commit()
