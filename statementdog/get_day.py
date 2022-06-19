from datetime import datetime


def get_today_stock_format():
    today = datetime.today().strftime("%Y%m%d")
    today_chinese = str(int(datetime.today().strftime("%Y%m%d")) - 19110000)
    return f"""{today_chinese[0:3]}/{today_chinese[3:5]}/{today_chinese[5:7]}"""
