import json
import pandas as pd
import requests as r
from datetime import datetime
import concurrent.futures
from get_free_ip import get_free_ip_dict
from get_day import get_today_stock_format


def get_stock_diff(ticker):
    today_date_chinese = "111/06/17"
    error_status = 1
    # date = datetime.datetime.today()
    date = "20220617"
    url = (
        f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?date={date}&stockNo={ticker}"
    )
    while error_status:
        try:
            proxies = get_free_ip_dict(https="yes")
            resp = r.get(url, proxies=proxies, timeout=5)
            js = json.loads(resp.text)
            print(ticker)
            for data in js["data"]:
                if data[0] == today_date_chinese:
                    return [ticker, data[-2]]
                    error_status = 0
                    continue
        except:
            error_status = 1


def get_stock_price_df(listed_data_path):
    success_list = []
    df_listed = pd.read_json(listed_data_path)
    ticker_list = df_listed["ticker"].to_list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for success_item in executor.map(get_stock_diff, ticker_list):
            success_list.append(success_item)
    df_diff = pd.DataFrame(success_list, columns=["ticker", "diff"])
    df_diff["diff"] = df_diff["diff"].apply(lambda x: float(x))
    return df_diff


if __name__ == "__main__":
    listed_data_path = "/Users/Desktop/statementdog/listed.json"
    df_diff = get_stock_price_df(listed_data_path)
    df_listed = pd.read_json(listed_data_path)
    df_listed["ticker"] = df_listed["ticker"].apply(lambda x: str(x))
    df_diff["ticker"] = df_diff["ticker"].apply(lambda x: str(x))
    df_merge = df_listed.merge(df_diff, how="inner", on="ticker")
    df_sorted = df_merge.sort_values(by=["diff"], ascending=False)
    df_top3 = df_sorted.groupby(by="industry").head(3)
    industry_list = list(set(df_listed["industry"].to_list()))
    for industry in industry_list:
        df_top3[df_top3["industry"] == industry][["ticker", "diff"]].to_json(
            f"/Users/Desktop/statementdog/result/{industry}_top3.json",
            orient="records",
            force_ascii=False,
        )
