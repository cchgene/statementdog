import random
import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs


class HttpEnterError(Exception):
    pass


def get_free_ip_dict(https="yes"):
    resp = r.get("https://free-proxy-list.net/")
    soup = bs(resp.text, "lxml").find_all(class_="table table-striped table-bordered")[
        0
    ]
    df = pd.read_html(
        str(soup).replace(' class="table table-striped table-bordered"', "")
    )[0]
    df = df[(df["Https"] == https) & (df["Country"] == "United States")]
    df["Port"] = df["Port"].apply(lambda x: str(x))
    df["Ip_port"] = df["IP Address"] + ":" + df["Port"]
    ip_list = df["Ip_port"].tolist()
    if https == "yes":
        ip_dict = {"https": ip_list[random.randint(0, len(ip_list) - 1)]}
    elif https == "no":
        ip_dict = {"http": ip_list[random.randint(0, len(ip_list) - 1)]}
    else:
        raise HttpEnterError("please enter yes to use https, or enter no to use http")
    return ip_dict
