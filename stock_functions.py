# version: 0.02dev
# todo: create a file with all funtions
# todo: resing from TA-LIB (not working fine on all your server)





# MOMENTUM INDICATORS

def get_indicators_momentum_adx(period_list):
    # ADX Average directional movement index
    # checked with tradingview
    # use only combined with other indicators
    for i in period_list:
        df["adx_"+str(i)] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=i)


def get_indicators_momentum_adxr(period_list):
    # ADXR Average directional movement index rating
    for i in period_list:
        df["adxr_"+str(i)] = ta.ADXR(df["high"], df["low"], df["close"], timeperiod=i)



def get_indicators_momentum_apo():
    # verification: apo_10_20 ok, other based on ta-lib not, but check them
    # name: Absolute price oscillator
    # interpretation: bearish market or bullish market
    # crossing above 0 - bullish ; crossing below 0 - berish
    # APO = Shorter Period EMA – Longer Period EMA
    # problems: talib and pt-lib calculations are not pass with pattern
    # require: EMA's
    df["apo_10_20"] = df["ema_10"] - df["ema_20"]  # standard
    df["apo_talib_10_20"] = ta.APO(df["close"], fastperiod=10, slowperiod=20, matype=0)  # standart tradingview
    df["apo_talib_12_26"] = ta.APO(df["close"], fastperiod=12, slowperiod=26, matype=0)



def get_indicators_momentum_apo_cross():
    # verification: apo_cross_10_20 ok, other based on ta-lib not, but check them
    # token
    # 1 - crossing to bullish ; 0 - crossing to bearish
    df["apo_cross_10_20"] = np.where((df["apo_10_20"] > 0) & (df["apo_10_20"].shift(1) < 0), 1,
                                     np.where((df["apo_10_20"] < 0) & (df["apo_10_20"].shift(1) > 0), -1, 0))
    df["apo_cross_talib_10_20"] = np.where((df["apo_talib_10_20"] > 0) & (df["apo_talib_10_20"].shift(1) < 0), 1,
                                     np.where((df["apo_talib_10_20"] < 0) & (df["apo_talib_10_20"].shift(1) > 0),
                                              -1, 0))
    df["apo_cross_talib_12_26"] = np.where((df["apo_talib_12_26"] > 0) & (df["apo_talib_12_26"].shift(1) < 0), 1,
                                     np.where((df["apo_talib_12_26"] < 0) & (df["apo_talib_12_26"].shift(1) > 0),
                                              -1, 0))


def get_indicators_momentum_aroon(period_list):
    # https://tradersarea.pl/aroon-indicator-wskaznik-analizy-technicznej/
    #AROON
    # verification:
    # tradingView: ok

    for i in period_list:
        df["aroondown_"+str(i)], df["aroonup_"+str(i)] = ta.AROON(df["high"], df["low"], timeperiod=i)

        #AROONOSC
        df["aroonosc_"+str(i)] = ta.AROONOSC(df["high"], df["low"], timeperiod=i)

def get_indicators_momentum_bop(period_list):
    # BOP - Balance Of Power
    # checked with tradingview
    df["bop"] = pta.bop(df["open"], df["high"], df["low"], df["close"])

    # BOP - Balance Of Power smoothed
    # autor: token
    for i in period_list:
        df["bop_sma_" + str(i)] = pta.sma(df["bop"], length=i)

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