import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)
web_page_source = driver.page_source
driver.quit()

df = pd.read_html(web_page_source)[0]
regex = re.compile("(\D)*")
for number in range(df.shape[0]):
    if len(regex.match(df.iloc[number, 0])[0]) > 0:
        if df.iloc[number, 0] == "股票":
            stock_start = number + 1
        elif df.iloc[number, 0] == "上市認購(售)權證":
            stock_end = number

df_rename = df[stock_start:stock_end].rename(
    columns={
        0: "ticker_name",
        1: "free3",
        2: "listed_at",
        3: "status",
        4: "industry",
        5: "free",
        6: "free2",
    }
)
regex_ticker = re.compile("(\d)*")
df_rename["ticker"] = df_rename["ticker_name"].map(
    lambda x: regex_ticker.match(x).group()
)
df_rename["name"] = df_rename["ticker_name"].map(
    lambda x: x.split(regex_ticker.match(x).group())[1].strip()
)
df_listed = df_rename[["ticker", "name", "listed_at", "industry"]]
df_listed.to_json(
    "/Users/Desktop/statementdog/listed.json", orient="records", force_ascii=False
)
