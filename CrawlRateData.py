import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

def url_get_contents(url):
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

def get_deposit_rate():
    xhtml = url_get_contents(
        'https://timo.vn/tai-khoan-tiet-kiem/lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat/').decode(
        'utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)

    deposit_rate = pd.DataFrame(p.tables[0])
    deposit_rate.columns = deposit_rate.iloc[0]
    deposit_rate = deposit_rate[1:]
    deposit_rate.head()
    deposit_rate = format_data(deposit_rate)
    
    return deposit_rate

def get_loan_rate():
    r = requests.get("https://money24h.vn/lai-suat-vay-ngan-hang")
    soup = BeautifulSoup(r.text,'html.parser')
    div = soup.select("#__NEXT_DATA__")[0].text

    jsonObj = json.loads(div)["props"]["pageProps"]["loanRateAllBank"]

    for item in jsonObj:
        item["results"] = item["results"]["result"]

    df = pd.DataFrame(jsonObj)[['bankName','results']]
    df.rename(columns= lambda col: col.replace("bankName", "Bank").replace("results","Rate"),inplace= True)

    return df

def format_data(data):
    df = pd.DataFrame(data)
    print(type(df))
    df.rename(columns= lambda col: col.replace("Ngân hàng", "Bank").replace("01 tháng", " 01 month").replace("tháng", "months"),inplace= True)

    return df
