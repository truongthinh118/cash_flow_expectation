import pandas as pd
import urllib.request
from html_table_parser.parser import HTMLTableParser

def url_get_contents(url):
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

def backup_deposit_rate():
    xhtml = url_get_contents(
        'https://timo.vn/tai-khoan-tiet-kiem/lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat/').decode(
        'utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)

    deposit_rate = pd.DataFrame(p.tables[0])
    deposit_rate.columns = deposit_rate.iloc[0]
    deposit_rate = deposit_rate[1:]
    deposit_rate.head()
    # deposit_rate = format_data(deposit_rate)
    return deposit_rate

# df = backup_deposit_rate()
# print (df)

a = 12
b = 5
print(a//b)