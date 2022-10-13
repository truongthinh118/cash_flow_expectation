import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd


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

def format_data(data):
    df = pd.DataFrame(data)
    print(type(df))
    df.rename(columns= lambda col: col.replace("Ngân hàng", "Bank").replace("01 tháng", " 01 month").replace("tháng", "months"),inplace= True)

    return df