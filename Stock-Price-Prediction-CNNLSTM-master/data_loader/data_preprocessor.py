"""
All non-neural data preprocessing.

Technical indicators:

MA - moving average
EMA - exponential moving average
MOM - momentum
ROC - rate of change
ATR - average true range
BBands - bollinger bands
RSI - relative strength index
MACD - Moving Average Convergence Divergencew
william_r_% - Williams Percent Range
k% - slow stochastic indicator
D% - fast stochastic indicator
A/D - accumulation/distribution


"""
import os
import numpy as np
import pandas as pd
import glob
# import talib as ta

# import still works even though the error message persists
import technical_indicators as ti


# TODO: derive adjusted Open, High, Low from the downloaded data. Save back to file.
def extract_features(fname_in=os.path.join("data_loader/original_data/indices/SPY.csv"), features_col= None, start=None, end=None, index="Date", economic=False):

    # create an processed data folder
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')

    # get the data set from fname
    # has to use csv if the file is in csv format
    df = pd.read_csv(fname_in)
    df = df.set_index(index)

    # select a time frame
    if start is None and end is None:
        df = df
    elif start is None and end is not None:
        df = df.loc[:end]
    elif start is not None and end is None:
        df = df.loc[start:]
    else:
        df = df[start:end]

    # call the technical functions in here

    print(df.head)
    # save the modified excel file
    # df.to_csv("original_data/SPY2.csv")
    # write a loop to load all the technical_indicators
    # df = ti.exponential_moving_average(df,2,3)
    # df = ti.moving_average(df,2,3)
    # df = ti.rate_of_change(df,1)
    # df = ti.future_moving_average(df, 2)
    # df = ti.future_exponential_moving_average(df, 2)

    for feature in features_col:
        s = feature.lower().split("_")

        if s[0] == "sma":
            df = ti.moving_average(df, int(s[1]), int(s[2]))
        if s[0] == "ema":
            df = ti.exponential_moving_average(df, int(s[1]), int(s[2]))
        if s[0] == "fsma":
            df = ti.future_moving_average(df, int(s[1]))
        if s[0] == "fema":
            df = ti.future_exponential_moving_average(df, int(s[1]))
        if s[0] == "roc":
            df = ti.rate_of_change(df, int(s[1]))
        if s[0] == "mom":
            df = ti.momentum(df, int(s[1]))
        if s[0] == "atr":
            df = ti.average_true_range(df, int(s[1]))

        if s[0] == "bb":

            if s[1] == "ub":
                df= ti.bollinger_bands_ub(df,int(s[2]))

            if s[1] == "mb":
                df = ti.bollinger_bands_mb(df, int(s[2]))

            if s[1] == "lb":
                df = ti.bollinger_bands_lb(df, int(s[2]))

        if s[0] == "rsi":
            df = ti.relative_strength_index(df, int(s[1]))

        if s[0] == "macd":

            if s[1] == "macd":
                df = ti.MACD_macd(df)
            if s[1] == "signal":
                df = ti.MACD_signal(df)
            if s[1] == "hist":
                df = ti.MACD_hist(df)

        if s[0] == "wr":
            df = ti.william_r(df, int(s[1]))
        if s[0] == "stocha":

            if s[1] == "k":
                df = ti.stocha_osc_d(df)
            if s[1] == "d":
                df = ti.stocha_osc_k(df)

        if s[0] == "acc":
            df = ti.acc_dist(df)

    # # call the economic functions in here
    all_econ_columns = []
    if economic == True:
        df, all_econ_columns = append_indices(df)

    # df.to_csv("data_loader/processed_data/tsla_processed.csv")
    print(df.head)
    # save the modified excel file
    # processed_file_name = os.path.basename(fname_in).split(".")
    # new_file_name = processed_file_name[0] + "_processed" + "." + processed_file_name[1]
    # df.to_csv(os.path.join("processed_data", new_file_name))
    return df.dropna(), all_econ_columns

def append_indices(df):
    # this function will append all the indices from the indices folder
    all_columns = []
    for fname in glob.glob('data_loader/original_data/econfactor/*.csv'):
        # print(fname)
        df_i = pd.read_csv(fname)
        df = match(df, df_i, os.path.basename(fname))
        all_columns.append(os.path.basename(fname))
        # print(df_i.shape,df.shape)
    return df, all_columns


# helper function for aligning feature data against the data of interest in this case SPY
def match(sp_df, df_i, nam):
    # fill missing data by extending previous day's day
    df_i = df_i.fillna(method='pad')

    # select only the closing price for further processing
    df_i = df_i.loc[:, ["Date", "Close"]]
    df_i = df_i.rename(columns={"Close": nam})

    # merge the usd index into s&p500 based on the 'Date' column
    # The method will remove the entries in usd index that did not appear in s&p500

    df_merged = pd.merge(sp_df, df_i, how="inner", on=["Date"])

    if df_merged.shape[0]<sp_df.shape[0]:
        df_merged = pd.merge(sp_df, df_merged.loc[:, ["Date", nam]], how="outer", on=["Date"])
        df_merged = df_merged.fillna(method ="pad")

    return df_merged


if __name__ == "__main__":
    # fname = "/home/guanyush/Pictures/CSC2516/CNNLSTM/data_loader/processed_data/kibot.csv"
    # extract_features(fname, index="Unnamed: 0", economic=False)

    fname = os.path.join("original_data/indices/TSLA.csv")
    extract_features(fname, features_col=["ROC_1"])
