# todo: update and lock records
# todo: zero-devide error in data frame
"""
pip install mysql-connector-python
pip install pandas
pip install numpy
plan 2022/02/03
"""
# libs
# import datetime
from db_works import db_connect
import pandas as pd
import numpy as np
import pandas_ta as pta  # https://mrjbq7.github.io/ta-lib/
import talib as ta  # install from whl file < https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import json
import time
import os
import uuid  # https://docs.python.org/3/library/uuid.html
import openpyxl


# todo: make better. All from json
# get settings from config json
def get_settings_json():
    with open("global_config.json") as json_conf:
        app_conf = (json.load(json_conf))
    print("conf file opened")
    db_tactics_schema_name = app_conf["db_tactics_schema_name"]
    db_klines_anl_table_name = app_conf["db_klines_anl_table_name"]
    db_binance_settings_table_name = app_conf["db_binance_settings_table_name"]
    db_tactics_table_name = app_conf["db_tactics_table_name"]
    db_tactics_analyse_table_name = app_conf["db_tactics_analyse_table_name"]
    db_tactics_results_table_name = app_conf["db_tactics_results_table_name"]
    TMP_DIR_PATH = app_conf["tmp_dir_path"]
    TACTICS_PACK_SIZE = app_conf["tactics_pack_size"]
    return db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE

# create temporary directory for downloaded files
def create_temp_dir():
    try:
        os.mkdir(TMP_DIR_PATH)
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



def get_tactics_to_check():
    cursor.execute("SELECT tactic_id, download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, "
                   "buy_indicator_1_operator,  yield_expected, wait_periods "
                   "FROM " + db_tactics_schema_name + "." + db_tactics_analyse_table_name + "  where tactic_status_id = 0 and download_settings_id = (SELECT download_settings_id FROM " + db_tactics_schema_name + "." + db_tactics_analyse_table_name + "  where tactic_status_id = 0 limit 1 )  limit " + str(TACTICS_PACK_SIZE) +" ")
    tactics_data = cursor.fetchall()
    return tactics_data

# download OHLC data from DWH
def get_ohlc_data():
    cursor.execute("SELECT * FROM " + db_tactics_schema_name + "." + db_klines_anl_table_name + " where "
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
    # basics
    df["open_time_dt"] = pd.to_datetime(df["open_datetime"], unit='ms')
    df["open_time_yr"] = df["open_time_dt"].dt.year
    df["open_time_mnt"] = df["open_time_dt"].dt.month
    df["open_time_dy"] = df["open_time_dt"].dt.day

    df["change_val"] = df.close - df.open
    df["change_perc"] = df.close / df.open - 1
    df["amplitude_val"] = df.high - df.low
    df["amplitude_perc"] = df.high - df.low / df.open
    df["up_down"] = np.where(df["close"] - df["close"].shift(1) > 0, 1, -1)


def get_indicators_trend_and_changes():
    # token: trend up/down 1 / -1
    # definition: in custom period sums of change are up or down.
    # you an combine it with ADX - trend strength by multiply both ie. -1 * 40
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
    # SMA (Simple), WMA, EMA (Exponential)
    for i in period_list:
        df["sma_"+str(i)] = pta.sma(df["close"], length=i)
        df["wma_"+str(i)] = pta.wma(df["close"], length=i)
        df["ema_"+str(i)] = pta.ema(df["close"], length=i)

def get_indicators_averages_cross():

    # Moving average crossing moving average
    # golden cross (1) and death cross (-1)
    df["cross_sma_50_200"] = np.where((df["sma_50"] - df["sma_200"] < 0) & (df["sma_50"].shift(1) - df["sma_200"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_50"] - df["sma_200"] > 0) & (df["sma_50"].shift(1) - df["sma_200"].shift(1) < 0), 1, 0)
    df["cross_sma_7_14"] = np.where((df["sma_7"] - df["sma_14"] < 0) & (df["sma_7"].shift(1) - df["sma_14"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_14"] > 0) & (df["sma_7"].shift(1) - df["sma_14"].shift(1) < 0), 1, 0)
    df["cross_sma_7_21"] = np.where((df["sma_7"] - df["sma_21"] < 0) & (df["sma_7"].shift(1) - df["sma_21"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_21"] > 0) & (df["sma_7"].shift(1) - df["sma_21"].shift(1) < 0), 1, 0)
    df["cross_sma_7_50"] = np.where((df["sma_7"] - df["sma_50"] < 0) & (df["sma_7"].shift(1) - df["sma_50"].shift(1) > 0), -1, 0) +\
                             np.where((df["sma_7"] - df["sma_50"] > 0) & (df["sma_7"].shift(1) - df["sma_50"].shift(1) < 0), 1, 0)

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

def get_indicators_averages_cross_perioids():
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


# MOMENTUM INDICATORS

def get_indicators_momentum_adx(period_list):
    # ADX Average directional movement index
    # checked with tradingview
    for i in period_list:
        df["adx_"+str(i)] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=i)


def get_indicators_momentum_adxr(period_list):
    # ADXR Average directional movement index rating
    for i in period_list:
        df["adxr_"+str(i)] = ta.ADXR(df["high"], df["low"], df["close"], timeperiod=i)



def get_indicators_momentum_apo():
    df["apo_12_26"] = pta.apo(df["close"], fastperiod=12, slowperiod=26, matype=0)  # standart
    df["apo_10_20"] = pta.apo(df["close"], fastperiod=10, slowperiod=20, matype=0)  # standart


def get_indicators_momentum_aroon(period_list):
    # https://tradersarea.pl/aroon-indicator-wskaznik-analizy-technicznej/
    #AROON
    for i in period_list:
        df["aroondown_"+str(i)], df["aroonup_"+str(i)] = ta.AROON(df["high"], df["low"], timeperiod=i)

        #AROONOSC
        df["aroonosc_"+str(i)] = ta.AROONOSC(df["high"], df["low"], timeperiod=i)

def get_indicators_momentum_bop():
    # BOP - Balance Of Power
    # checked with tradingview
    df["bop"] = pta.bop(df["open"], df["high"], df["low"], df["close"])

def get_indicators_momentum_cci(period_list):
    # CCI -- tradingView.. Oversold: -80 - -300/-500 - infinity scale
    for i in period_list:
        df["cci_"+str(i)] = ta.CCI(df["high"], df["low"], df["close"], i)

def get_indicators_momentum_cmo(period_list):
    #CMO - Chande Momentum Oscillator
    for i in period_list:
        df["cmo_"+str(i)] = pta.cmo(df["close"], timeperiod=i)

def get_indicators_momentum_dx(period_list):
    # DX - Directional Movement Index
    for i in period_list:
        df["dx_"+str(i)] = ta.DX(df["high"], df["low"], df["close"], timeperiod=i)


def get_indicators_momentum_macd():

    # MACD
    df["macd"], df["macdsignal"], df["macdhist"] = ta.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
    # 1- buy signal -1  sell signal
    df["upcross_downcross_macd_signal"] = np.where((df["macd"] - df["macdsignal"] > 0) & (df["macd"].shift(1) - df["macdsignal"].shift(1) < 0), 1, 0) +\
                             np.where((df["macd"] - df["macdsignal"] < 0) & (df["macd"].shift(1) - df["macdsignal"].shift(1) > 0), -1, 0)


# todo: MACDEXT - MACD with controllable MA type

# todo: MACDFIX - Moving Average Convergence/Divergence Fix 12/26


def get_indicators_momentum_mfi(period_list):
    # MFI - Money Flow Index
    for i in period_list:
        df["mfi_"+str(i)] = ta.MFI(df["high"], df["low"], df["close"], df["volume"], timeperiod=i)



def get_indicators_momentum_minus_di(period_list):
    # MINUS_DI - Minus Directional Indicator
    for i in period_list:
        df["minus_di_"+str(i)] = ta.MINUS_DI(df["high"], df["low"], df["close"], timeperiod=i)


def get_indicators_momentum_minus_dm(period_list):
    # MINUS_DM - Minus Directional Movement
    for i in period_list:
        df["minus_dm_"+str(i)] = ta.MINUS_DM(df["high"], df["low"], timeperiod=i)


def get_indicators_momentum_mom(period_list):
    # MOM - Momentum
    for i in period_list:
        df["mom_"+str(i)] = ta.MOM(df["close"], timeperiod=i)


def get_indicators_momentum_plus_di(period_list):
    # MINUS_DI - Minus Directional Indicator (negative)
    for i in period_list:
        df["plus_di_"+str(i)] = ta.PLUS_DI(df["high"], df["low"], df["close"], timeperiod=i)


def get_indicators_momentum_plus_dm(period_list):
    # MINUS_DM - Minus Directional Movement (positive)
    for i in period_list:
        df["plus_dm_"+str(i)] = ta.PLUS_DM(df["high"], df["low"], timeperiod=i)


def get_indicators_momentum_ppo():
    # PPO - Percentage Price Oscillator
    df["ppo_12_26"] = ta.PPO(df["close"], fastperiod=12, slowperiod=26, matype=0)  # standart
    df["ppo_10_21"] = ta.PPO(df["close"], fastperiod=10, slowperiod=21, matype=0)  # tradingview corr


def get_indicators_momentum_roc(period_list):
    # ROC - Rate of change : ((price/prevPrice)-1)*100
    for i in period_list:
        df["roc_"+str(i)] = ta.ROC(df["close"], timeperiod=i)

def get_indicators_momentum_rocp(period_list):
    # ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
    for i in period_list:
        df["rocp_"+str(i)] = ta.ROCP(df["close"], timeperiod=i)

def get_indicators_momentum_rocr(period_list):
    # ROCR - Rate of change ratio: (price/prevPrice)
    for i in period_list:
        df["rocr_"+str(i)] = ta.ROCR(df["close"], timeperiod=i)

def get_indicators_momentum_rocr100(period_list):
    # ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
    for i in period_list:
        df["rocr100_"+str(i)] = ta.ROCR100(df["close"], timeperiod=i)

def get_indicators_momentum_rsi(period_list):
    # RSI - Relative Strength Index
    for i in period_list:
        df["rsi_"+str(i)] = ta.RSI(df["close"], timeperiod=i)


def get_indicators_momentum_stoch():
    # STOCH - Stochastic
    df["slowk"], df["slowd"] = ta.STOCH(df["high"], df["low"], df["close"], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

def get_indicators_momentum_stochf():
    # STOCHF - Stochastic Fast
    df["fastk"], df["fastd"] = ta.STOCHF(df["high"], df["low"], df["close"], fastk_period=5, fastd_period=3, fastd_matype=0)

def get_indicators_momentum_stochrsi(period_list):
    # STOCHRSI - Stochastic Relative Strength Index
    for i in period_list:
        df["stochrsi_fast_k_"+str(i)], df["stochrsi_fast_d_"+str(i)] = ta.STOCHRSI(df["close"], timeperiod=i, fastk_period=5, fastd_period=3, fastd_matype=0)


def get_indicators_momentum_trix(period_list):
    # TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
    # 30 standard time period
    for i in period_list:
        df["trix_"+str(i)] = ta.TRIX(df["close"], timeperiod=i)

def get_indicators_momentum_ultosc():
    # ULTOSC - Ultimate Oscillator
    df["ultosc_7_14_28"] = ta.ULTOSC(df["high"], df["low"], df["close"], timeperiod1=7, timeperiod2=14, timeperiod3=28)




def get_indicators_momentum_willr(period_list):
    for i in period_list:
        df["willr_"+str(i)] = ta.WILLR(df["high"], df["low"], df["close"], timeperiod=i)


# todo: indicators outside TA-LIB (fe. CHOP, other from trafing course FXMAG (aligators etc.)


# VOLUME INDICATORS

def get_indicators_volume_chaikin_ad():
    df["chaikin_ad"] = ta.AD(df["high"], df["low"], df["close"], df["volume"])

def get_indicators_volume_chaikin_ad_oscillator():
    df["chaikin_ad_oscillator_3_10"] = ta.ADOSC(df["high"], df["low"], df["close"], df["volume"], fastperiod=3, slowperiod=10)

def get_indicators_volume_obv():
    df["chaikin_obv"] = ta.OBV(df["close"], df["volume"])


# PRINT RESULTS
def print_results():
    print(df)

# EXPORT TO EXCEL
def export_results_to_xls():
    df.to_excel("exports/export_settings" + str(download_settings_id) + "_" + str(time.time()) + ".xlsx")




if __name__ == "__main__":
    db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name\
        , db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = get_settings_json()
    create_temp_dir()
    # delete_old_files()
    cursor, cnxn = db_connect()
    #

    open_time = str(1531042226) + '000'
    tactics_data = get_tactics_to_check()
    download_settings_id = tactics_data[0][1]
    # print(tactics_data)

    print("select done settings done")


    # todo: not need to use all params. just use download_settings_id
    # todo: combination table. Can be stored in other schema

    # TEST VALUES
    # download_settings_id = 11  # 3
    # market = 'BTCUSDT'
    # tick_interval = '1d'
    # data_granulation = 'klines'
    # stock_type = 'spot'
    # stock_exchange = 'Binance.com'
    # open_time = str(1631042226) + '000'


    df, df_bak = get_ohlc_data()
    print(df)

    tactics_data = get_tactics_to_check()

    get_structured_data()
    print(df)


    # INDICATORS

    get_indicators_basics()
    #get_indicators_trend_and_changes()
    #get_indicators_averages([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_averages_cross()
    #get_indicators_averages_cross_perioids()

    #get_indicators_momentum_adx([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_adxr([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_apo()
    #get_indicators_momentum_aroon([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_bop()
    #get_indicators_momentum_cci([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_cmo([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_dx([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_macd()
    #get_indicators_momentum_mfi([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])  # tradingview checked:ok
    #get_indicators_momentum_minus_di([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_minus_dm([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_mom([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_plus_di([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_plus_dm([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_ppo()
    #get_indicators_momentum_roc([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])  # tradingview checked:ok
    #get_indicators_momentum_rocp([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_rocr([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_rocr100([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    get_indicators_momentum_rsi([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_stoch()
    #get_indicators_momentum_stochf()
    #get_indicators_momentum_stochrsi([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_trix([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])
    #get_indicators_momentum_ultosc()
    #get_indicators_momentum_willr([7, 9, 12, 14, 20, 21, 24, 25, 30, 50, 100, 200])

    # Volume indicators
    #get_indicators_volume_chaikin_ad()
    #get_indicators_volume_chaikin_ad_oscillator()
    #get_indicators_volume_obv()

    print(df)

    # todo: if some results are different between tradingview and this program - check other library fe: TA instead of PTA

    # export_results_to_xls()

    print_results()
