import os
import json
import numpy as np
import pandas as pd
import requests as r
from datetime import datetime
import concurrent.futures
from get_free_ip import get_free_ip_dict
from get_day import get_today_stock_format


def get_stock_diff(ticker):
    # today_date_chinese = get_today_stock_format()
    output_path = f"{base_path}/tmp"
    today_date_chinese = "111/06/17"
    error_status = 1
    date = "20220617"
    url = (
        f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?date={date}&stockNo={ticker}"
    )
    while error_status:
        try:
            proxies = get_free_ip_dict(https="yes")
            resp = r.get(url, proxies=proxies, timeout=5)
            js = json.loads(resp.text)
            if js["stat"] == "OK":
                for data in js["data"]:
                    if data[0] == today_date_chinese:
                        pass
            else:
                data = [None, None]
            with open(f"{output_path}/{ticker}.txt", "w") as f:
                f.write(f"{ticker}, {data[-2]}")
            error_status = 0
        except r.exceptions.ConnectionError:
            error_status = 1


def get_stock_price(ticker_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        executor.map(get_stock_diff, ticker_list)


def get_done_ticker_list():
    for done_ticker in os.walk(f"{base_path}/statementdog/tmp/"):
        done_ticker_list = [ticker.replace(".txt", "") for ticker in done_ticker[2]]
    return done_ticker_list


def get_stock_diff_df(ticker_diff_file_path):
    total_data = []
    for ticker_diff_file in os.listdir(ticker_diff_file_path):
        with open(f"{ticker_diff_file_path}/{ticker_diff_file}", "r") as f:
            if ticker_diff_file != ".DS_Store":
                data = [raw_data.strip() for raw_data in f.read().split(",")]
                total_data.append(data)
    stock_diff_df = pd.DataFrame(total_data, columns=["ticker", "diff"])
    stock_diff_df["diff"] = stock_diff_df["diff"].apply(lambda x: convert_to_float(x))
    return stock_diff_df


def convert_to_float(data):
    if data == "None":
        data = np.NaN
    elif data[0] == "X":
        data = np.NaN
    else:
        data = float(data)
    return data


def get_run_ticker_list(ticker_list):
    done_ticker_list = get_done_ticker_list()
    run_ticker_list = list(set(ticker_list) - set(done_ticker_list))
    return run_ticker_list


def get_top3_df(df_listed, stock_diff_df):
    df_listed["ticker"] = df_listed["ticker"].apply(lambda x: str(x))
    df_merge = df_listed.merge(stock_diff_df, how="inner", on="ticker")
    df_sorted = df_merge.sort_values(by=["diff"], ascending=False)
    df_top3 = df_sorted.groupby(by="industry").head(3)
    df_top3["diff"] = df_top3["diff"].apply(lambda x: str(x) + "%")
    return df_top3


def ouptut_industry_to_json(df_listed, df_top3, output_path):
    industry_list = list(set(df_listed["industry"].to_list()))
    for industry in industry_list:
        df_top3[df_top3["industry"] == industry][["ticker", "diff"]].to_json(
            f"{output_path}/{industry}_top3.json",
            orient="records",
            force_ascii=False,
            indent=4,
        )


if __name__ == "__main__":
    base_path = "/Users/Desktop/statementdog"
    listed_data_path = f"{base_path}/result/listed.json"
    df_listed = pd.read_json(listed_data_path)
    ticker_list = [str(ticker) for ticker in df_listed["ticker"].to_list()]

    run_ticker_list = get_run_ticker_list(ticker_list)
    while len(run_ticker_list) != 0:
        get_stock_price(run_ticker_list)
        run_ticker_list = get_run_ticker_list(ticker_list)

    ticker_diff_file_path = f"{base_path}/statementdog/tmp"
    stock_diff_df = get_stock_diff_df(ticker_diff_file_path)
    df_top3 = get_top3_df(df_listed, stock_diff_df)
    output_path = f"{base_path}/result"
    ouptut_industry_to_json(df_listed, df_top3, output_path)
